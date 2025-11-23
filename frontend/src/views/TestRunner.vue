<template>
  <div>
    <TopBar />

    <div class="container py-5 d-flex justify-content-center">
      <div class="w-100" style="max-width: 700px;">

        <!-- Test-Titel -->
        <h1 class="text-center mb-4" style="padding-top: 50px;">
          {{ test.title }}
        </h1>

        <!-- Progress-Bar -->
        <div class="d-flex justify-content-center gap-2 mb-4">
          <button
            v-for="(item, i) in testItems"
            :key="item.guid"
            class="btn rounded-circle"
            :class="{
              'btn-primary':         !isReviewMode && i === currentIndex,
              'btn-outline-secondary': !isReviewMode && i !== currentIndex,
              'btn-success':         isReviewMode && isCorrect(i),
              'btn-danger':          isReviewMode && !isCorrect(i)
            }"
            style="width: 40px; height: 40px;"
            @click="goTo(i)"
          >
            {{ i + 1 }}
          </button>
        </div>

        <!-- Karte mit Player + Navigation / Review-Info -->
        <div class="card mb-5 p-4 border rounded item-player-card">

          <!-- Frage-Titel aus XML -->
          <h2 class="text-center text-uppercase mb-3">
            {{ getTitleFromXml(currentItem.xml) }}
          </h2>

          <!-- QTI3 Player -->
          <div class="player-wrapper mb-4">
            <Qti3Player
              ref="qti3player"
              @notifyQti3PlayerReady="onPlayerReady"
              @notifyQti3SuspendAttemptCompleted="onItemSaved"
              @notifyQti3EndAttemptCompleted="onItemSaved"
              @notifyQti3ScoreAttemptCompleted="onItemSaved"
            />
          </div>

          <!-- Im Review-Modus: Richtige Antwort anzeigen -->
          <div v-if="isReviewMode" class="text-center mb-3">
            <strong>Correct Answer:</strong>
            <span :class="{'text-success': isCorrect(currentIndex), 'text-danger': !isCorrect(currentIndex)}">
              {{ getCorrectAnswer(currentItem.guid) }}
            </span>
          </div>

          <!-- Navigation nur im normalen Modus -->
          <div v-if="!isReviewMode" class="d-flex justify-content-center gap-3 mt-2">
            <button class="btn btn-secondary" @click="prev" :disabled="currentIndex === 0">
              Previous
            </button>
            <button
              v-if="currentIndex < testItems.length - 1"
              class="btn btn-primary"
              @click="next"
              :disabled="!qti3player"
            >
              Next
            </button>
            <button
              v-else
              class="btn btn-danger"
              @click="submitTest"
              :disabled="!qti3player"
            >
              Submit
            </button>
          </div>

        </div>

        <!-- Zurück-Button im Review-Modus -->
        <div v-if="isReviewMode" class="text-center">
          <router-link :to="{ name: 'Home' }" class="btn btn-primary">
            Zurück zur Startseite
          </router-link>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import Qti3Player from 'qti3-item-player'
import 'qti3-item-player/dist/qti3Player.css'
import TopBar from '@/components/TopBar.vue';

export default {
  name: 'Test',
  components: { Qti3Player, TopBar },
  data() {
    return {
      qti3player: null,
      test: null,
      testItems: [],
      itemStates: new Map(),
      currentIndex: 0,
      isReviewMode: false,
      itemsLoaded: false,
      playerReady: false
    }
  },
  computed: {
    currentItem() {
      return this.testItems[this.currentIndex] || {};
    },
    currentState() {
      return this.itemStates.get(this.currentItem.guid) || null;
    }
  },
  methods: {
    async loadTest(id) {
      this.test = this.$testService.getTestById(id)
      this.testItems = await this.$testService.loadQuestionItems(this.test.items);
      this.itemsLoaded = true;
      this.tryLoadItem();
    },
    onPlayerReady(player) {
      this.qti3player = player;
      this.playerReady   = true;
      this.tryLoadItem();
    },
    tryLoadItem() {
      if (!this.playerReady || !this.itemsLoaded) return;
      this.loadCurrentItem();
    },
    loadCurrentItem() {
      const item = this.currentItem;
      if (!item.guid || !this.qti3player) return;

      const config = {
        guid: item.guid,
        status: this.isReviewMode ? 'review' : 'interacting',
        ...(this.currentState && { state: this.currentState })
      };

      this.qti3player.loadItemFromXml(item.xml, config);
    },

    next() {
      if (this.currentIndex < this.testItems.length - 1) {
        this.qti3player.suspendAttempt('next');
      }
    },
    prev() {
      if (this.currentIndex > 0) {
        this.qti3player.suspendAttempt('prev');
      }
    },
    submitTest() {
      this.qti3player.suspendAttempt('end');
    },

    onItemSaved(data) {
      this.itemStates.set(data.state.guid, data.state);

      switch (data.target) {
        case 'next':
          this.currentIndex++;
          this.loadCurrentItem();
          break;
        case 'prev':
          this.currentIndex--;
          this.loadCurrentItem();
          break;
        case 'end':
          console.log('--- All Item States kurz vor Review-Modus: ---');
          console.log(JSON.stringify(Object.fromEntries(this.itemStates), null, 2));
          // Wechsel in den Review-Modus
          this.isReviewMode = true;
          this.currentIndex = 0;
          this.loadCurrentItem();
          break;
      }
    },

    goTo(i) {
      this.currentIndex = i;
      this.loadCurrentItem();
    },

    // Prüft, ob Antwort richtig war
    isCorrect(idx) {
    const item  = this.testItems[idx];
    const state = this.itemStates.get(item.guid);
    if (!state) return false;

    // responseVariable zur RESPONSE
    const rv = state.responseVariables.find(v => v.identifier === 'RESPONSE');
    if (!rv) return false;

    const actual  = rv.value;           // kann String oder Array sein
    const correct = rv.correctResponse; // kann String oder Array sein

    // Multiple Choice?
    if (Array.isArray(correct)) {
      // actual muss auch Array sein
      if (!Array.isArray(actual)) return false;
      // Längen gleich?
      if (correct.length !== actual.length) return false;
      // jede korrekte ID muss im actual-Array vorkommen
      return correct.every(id => actual.includes(id));
    }

    // Single Choice: einfacher Vergleich
    return actual === correct;
  },

    getTitleFromXml(xmlString) {
      const parser = new DOMParser();
      const doc    = parser.parseFromString(xmlString, 'text/xml');
      return doc.querySelector('qti-assessment-item')?.getAttribute('title') || '';
    },
    getResponseValue(state) {
      return state.responseVariables.find(v => v.identifier === 'RESPONSE')?.value;
    },
    getCorrectAnswer(guid) {
    // 1) correctResponse aus dem State
    const state = this.itemStates.get(guid);
    const respVar = state
      ?.responseVariables
      .find(v => v.identifier === 'RESPONSE');
    if (!respVar || respVar.correctResponse == null) {
      return null;
    }

    // sorgen, dass wir immer mit einem Array weiterarbeiten
    const ids = Array.isArray(respVar.correctResponse)
      ? respVar.correctResponse
      : [respVar.correctResponse];

    // 2) XML parsen
    const item = this.testItems.find(i => i.guid === guid);
    if (!item?.xml) {
      // kein XML? dann gib die rohen IDs zurück
      return Array.isArray(respVar.correctResponse)
        ? [...ids]
        : ids[0];
    }
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(item.xml, 'text/xml');

    // 3) für jede ID den Text ermitteln
    const texts = ids.map(id => {
      const choice = xmlDoc.querySelector(`qti-simple-choice[identifier="${id}"]`);
      return choice
        ? choice.textContent.trim()
        : id;  // Fallback auf die ID
    });

    // Single vs. Multiple
    return Array.isArray(respVar.correctResponse)
      ? texts
      : texts[0];
  },

  },
  created() {
    //
  },
  mounted() {
    this.loadTest(this.$route.params.id);
  }
}
</script>

<style scoped>
.item-player-card {
  background-color: #f8f9fa;
  border-color: #dee2e6;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}
::v-deep(.player-wrapper *) {
  background-color: #f8f9fa;

}
</style>
