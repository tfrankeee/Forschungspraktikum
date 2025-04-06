<template>
  <main id="main" class="test-controller-container container-fluid">
    <div class="test-controller-content">
      <Qti3Player
        ref="qti3player"
        :container-class="'qti3-player-container-fluid'"
        :container-padding-class="'qti3-player-container-padding-2'"
        :color-class="'qti3-player-color-default'"
        suppress-alert-messages
        suppress-invalid-response-messages
        @notifyQti3PlayerReady="handlePlayerReady"
      />
    </div>
  </main>
</template>

<script>
import Qti3Player from "qti3-item-player"
import "qti3-item-player/dist/qti3Player.css"

export default {
  components: { Qti3Player },

  methods: {
    handlePlayerReady(player) {
      this.qti3Player = player

      const config = {
        guid: "frage001",
        status: "interacting"
      }

      fetch("questions/frage1.xml")
        .then((res) => res.text())
        .then((xml) => {
          this.qti3Player.loadItemFromXml(xml, config)
        })
    }
  }
}
</script>

<style>
/* Nur die minimalen Styles, die für den Wrapper nötig sind */
.test-controller-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.test-controller-content {
  margin: 10px 0;
  background: #f8f9fa; /* helles Bootstrap-Grau */
  flex: 1;
}
</style>
