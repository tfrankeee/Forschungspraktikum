<template>
  <div class="qti-player">
    <div v-if="loading">Loading question...</div>
    
    <div v-else-if="error" class="error">
      Error loading question: {{ error }}
    </div>
    
    <div v-else>
      <!-- Question Navigation -->
      <div class="question-nav">
        <button v-for="(q, index) in questionList" 
                :key="q.path" 
                @click="goToQuestion(index)"
                :class="{ 
                  active: currentIndex === index,
                  answered: userAnswers[index] !== undefined
                }">
          {{ index + 1 }}
        </button>
      </div>
      
      <!-- Question Display -->
      <div v-if="!testEnded" class="question-container">
        <h2>{{ questionTitle }}</h2>
        
        <!-- Single Choice -->
        <div v-if="questionType === 'single-choice'" class="choice-question">
          <p>{{ questionText }}</p>
          <div v-for="choice in choices" :key="choice.identifier" class="choice">
            <label>
              <input type="radio" 
                     v-model="userAnswers[currentIndex]" 
                     :value="choice.identifier">
              {{ choice.text }}
            </label>
          </div>
        </div>
        
        <!-- Multiple Choice -->
        <div v-else-if="questionType === 'multiple-choice'" class="choice-question">
          <p>{{ questionText }}</p>
          <div v-for="choice in choices" :key="choice.identifier" class="choice">
            <label>
              <input type="checkbox" 
                     v-model="userAnswers[currentIndex]" 
                     :value="choice.identifier"
                     @change="handleMultipleChoiceChange">
              {{ choice.text }}
            </label>
          </div>
        </div>
        
        <!-- String Answer -->
        <div v-else-if="questionType === 'string-answer'">
          <p>{{ questionText }}</p>
          <textarea v-model="userAnswers[currentIndex]" rows="3"></textarea>
        </div>
        
        <!-- Fill in Blank -->
        <div v-else-if="questionType === 'fill-blank'">
          <p v-html="fillBlankText"></p>
          <input type="text" v-model="userAnswers[currentIndex]">
        </div>
        
        <!-- True/False -->
        <div v-else-if="questionType === 'true-false'" class="choice-question">
          <p>{{ questionText }}</p>
          <div class="choice">
            <label>
              <input type="radio" v-model="userAnswers[currentIndex]" value="true"> True
            </label>
          </div>
          <div class="choice">
            <label>
              <input type="radio" v-model="userAnswers[currentIndex]" value="false"> False
            </label>
          </div>
        </div>
        
        <!-- Navigation Controls -->
        <div class="navigation-controls">
          <button @click="prevQuestion" :disabled="currentIndex === 0">Previous</button>
          
          <button 
            v-if="currentIndex !== questionList.length - 1"
            @click="nextQuestion"
          >
            Next
          </button>
          
          <button 
            v-if="currentIndex === questionList.length - 1"
            @click="endTest"
            class="submit-btn"
          >
            Submit
          </button>
          
          <button @click="endTest" class="end-test">End Test</button>
        </div>
      </div>
      
      <!-- Results Display -->
      <div v-else class="results">
        <h2>Test Results</h2>
        <div class="score-summary">
          <p>You scored {{ score.toFixed(2) }} out of {{ questionList.length }} ({{ percentage }}%)</p>
        </div>
        
        <div v-for="(question, index) in questionList" :key="index" class="question-result">
          <h3>Question {{ index + 1 }}: {{ question.title }}</h3>
          <div class="question-text">{{ questionsData[index].text }}</div>
          
          <div class="answer-comparison">
            <div class="user-answer">
              <strong>Your answer:</strong> 
              <span :class="getAnswerClass(index)">
                {{ displayUserAnswer(index) }}
              </span>
            </div>
            <div class="correct-answer">
              <strong>Correct answer:</strong> 
              {{ displayCorrectAnswer(index) }}
            </div>
            <div class="points-earned">
              <strong>Points:</strong> 
              {{ questionPoints[index].toFixed(2) }}/1
              <span v-if="questionPoints[index] > 0 && questionPoints[index] < 1" class="partial-credit">
                (Partial credit)
              </span>
            </div>
          </div>
        </div>
        
        <button @click="restartTest" class="restart-btn">Start New Test</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Qti3Player',
  data() {
    return {
      questionList: [
        { path: '/questions/single-choice.xml', title: 'Big-O Notation' },
        { path: '/questions/multiple-choice.xml', title: 'Data Structures' },
        { path: '/questions/string-answer.xml', title: 'Pascal Language' },
        { path: '/questions/fill-blank.xml', title: 'Boolean Algebra' },
        { path: '/questions/true-false.xml', title: 'Computer Architecture' }
      ],
      currentIndex: 0,
      questionsData: [],
      userAnswers: [],
      questionPoints: [],
      testEnded: false,
      loading: false,
      error: null
    }
  },
  computed: {
    currentQuestion() {
      return this.questionList[this.currentIndex];
    },
    questionType() {
      return this.questionsData[this.currentIndex]?.type || '';
    },
    questionTitle() {
      return this.questionsData[this.currentIndex]?.title || '';
    },
    questionText() {
      return this.questionsData[this.currentIndex]?.text || '';
    },
    choices() {
      return this.questionsData[this.currentIndex]?.choices || [];
    },
    fillBlankText() {
      return this.questionsData[this.currentIndex]?.fillBlankText || '';
    },
    score() {
      return this.questionPoints.reduce((total, points) => total + points, 0);
    },
    percentage() {
      return Math.round((this.score / this.questionList.length) * 100);
    }
  },
  async created() {
    await this.loadAllQuestions();
  },
  methods: {
    async loadAllQuestions() {
      this.loading = true;
      this.error = null;
      this.questionsData = [];
      this.userAnswers = Array(this.questionList.length).fill(undefined);
      this.questionPoints = Array(this.questionList.length).fill(0);
      
      try {
        for (const q of this.questionList) {
          const response = await fetch(q.path);
          const xmlText = await response.text();
          const parser = new DOMParser();
          const xmlDoc = parser.parseFromString(xmlText, "text/xml");
          
          const questionData = this.parseQuestion(xmlDoc, q.title);
          this.questionsData.push(questionData);
        }
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    
    parseQuestion(xmlDoc, title) {
      const questionData = {
        title,
        type: '',
        text: '',
        choices: [],
        correctAnswer: null,
        correctAnswers: [],
        fillBlankText: ''
      };
      
      const interaction = xmlDoc.querySelector('itemBody > *');
      
      if (interaction.tagName === 'choiceInteraction') {
        const maxChoices = parseInt(interaction.getAttribute('maxChoices'));
        questionData.type = maxChoices === 1 ? 'single-choice' : 'multiple-choice';
        questionData.text = interaction.querySelector('prompt').textContent;
        
        const choiceElements = interaction.querySelectorAll('simpleChoice');
        questionData.choices = Array.from(choiceElements).map(el => ({
          identifier: el.getAttribute('identifier'),
          text: el.textContent
        }));
        
        const correctResponses = xmlDoc.querySelectorAll('correctResponse value');
        if (questionData.type === 'single-choice') {
          questionData.correctAnswer = correctResponses[0].textContent;
        } else {
          questionData.correctAnswers = Array.from(correctResponses).map(r => r.textContent);
        }
      } 
      else if (interaction.tagName === 'extendedTextInteraction') {
        questionData.type = 'string-answer';
        questionData.text = interaction.querySelector('prompt').textContent;
        questionData.correctAnswer = xmlDoc.querySelector('correctResponse value').textContent;
      } 
      else if (interaction.tagName === 'textEntryInteraction') {
        questionData.type = 'fill-blank';
        const paragraph = interaction.parentElement;
        questionData.text = paragraph.textContent.replace('__________', '_________');
        questionData.fillBlankText = paragraph.innerHTML.replace('__________', 
          '<span class="blank-space">_________</span>');
        questionData.correctAnswer = xmlDoc.querySelector('correctResponse value').textContent;
      } 
      else if (interaction.tagName === 'choiceInteraction' && 
               interaction.querySelector('simpleChoice[identifier="true"]')) {
        questionData.type = 'true-false';
        questionData.text = interaction.querySelector('prompt').textContent;
        questionData.correctAnswer = xmlDoc.querySelector('correctResponse value').textContent;
      }
      
      return questionData;
    },
    
    goToQuestion(index) {
      this.currentIndex = index;
    },
    
    prevQuestion() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      }
    },
    
    nextQuestion() {
      if (this.currentIndex < this.questionList.length - 1) {
        this.currentIndex++;
      }
    },
    
    handleMultipleChoiceChange() {
      if (!Array.isArray(this.userAnswers[this.currentIndex])) {
        this.$set(this.userAnswers, this.currentIndex, []);
      }
    },
    
    endTest() {
      this.questionPoints = this.questionList.map((_, index) => 
        this.calculateQuestionPoints(index)
      );
      this.testEnded = true;
    },
    
    calculateQuestionPoints(index) {
      const userAnswer = this.userAnswers[index];
      const question = this.questionsData[index];
      
      if (userAnswer === undefined || userAnswer === null || userAnswer === '') {
        return 0;
      }
      
      switch (question.type) {
        case 'single-choice':
        case 'true-false': {
          return userAnswer === question.correctAnswer ? 1 : 0;
        }
          
        case 'multiple-choice': {
          if (!Array.isArray(userAnswer)) return 0;
          
          const totalCorrect = question.correctAnswers.length;
          const userCorrect = userAnswer.filter(ans => 
            question.correctAnswers.includes(ans)).length;
          const userIncorrect = userAnswer.filter(ans => 
            !question.correctAnswers.includes(ans)).length;
          
          return Math.max(0, (userCorrect - userIncorrect) / totalCorrect);
        }
          
        case 'string-answer': {
          if (userAnswer.trim().toLowerCase() === 'niklaus wirth') return 1;
          if (userAnswer.trim().toLowerCase() === 'wirth') return 0.8;
          return 0;
        }
          
        case 'fill-blank': {
          return userAnswer.trim().toLowerCase() === 'de morgan' ? 1 : 0;
        }
          
        default: {
          return 0;
        }
      }
    },
    
    restartTest() {
      this.userAnswers = Array(this.questionList.length).fill(undefined);
      this.questionPoints = Array(this.questionList.length).fill(0);
      this.currentIndex = 0;
      this.testEnded = false;
    },
    
    getAnswerClass(index) {
      return this.questionPoints[index] > 0 ? 'correct' : 'incorrect';
    },
    
    displayUserAnswer(index) {
      const userAnswer = this.userAnswers[index];
      const question = this.questionsData[index];
      
      if (userAnswer === undefined || userAnswer === null || userAnswer === '') {
        return 'No answer provided';
      }
      
      switch (question.type) {
        case 'single-choice':
        case 'true-false':
          return this.displayChoiceAnswer(userAnswer, question);
        case 'multiple-choice':
          return Array.isArray(userAnswer) 
            ? userAnswer.map(ans => this.displayChoiceAnswer(ans, question)).join(', ')
            : 'Invalid answer format';
        case 'string-answer':
        case 'fill-blank':
          return `"${userAnswer}"`;
        default:
          return userAnswer;
      }
    },
    
    displayCorrectAnswer(index) {
      const question = this.questionsData[index];
      
      switch (question.type) {
        case 'single-choice':
        case 'true-false':
          return this.displayChoiceAnswer(question.correctAnswer, question);
        case 'multiple-choice':
          return question.correctAnswers.map(ans => 
            this.displayChoiceAnswer(ans, question)).join(', ');
        case 'string-answer':
          return '"Niklaus Wirth" (1.0) or "Wirth" (0.8)';
        case 'fill-blank':
          return `"${question.correctAnswer}"`;
        default:
          return question.correctAnswer;
      }
    },
    
    displayChoiceAnswer(value, question) {
      if (question.type === 'true-false') {
        return value === 'true' ? 'True' : 'False';
      }
      const choice = question.choices.find(c => c.identifier === value);
      return choice ? choice.text : value;
    }
  }
}
</script>

<style scoped>
.qti-player {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.question-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
}

.question-nav button {
  width: 40px;
  height: 40px;
  padding: 0;
  border: 1px solid #ddd;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
}

.question-nav button.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.question-nav button.answered {
  background: #e1f5fe;
  border-color: #3498db;
}

.choice-question {
  margin: 15px 0;
}

.choice {
  margin: 8px 0;
  padding: 8px;
  background: #f9f9f9;
  border-radius: 4px;
}

label {
  cursor: pointer;
}

textarea, input[type="text"] {
  width: 100%;
  padding: 8px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.navigation-controls {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 30px;
}

.navigation-controls button {
  padding: 8px 16px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.navigation-controls button:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

.submit-btn {
  background: #2ecc71 !important;
  margin-right: auto;
}

.end-test {
  background: #e74c3c !important;
}

.results {
  margin-top: 20px;
}

.score-summary {
  font-size: 1.2em;
  margin-bottom: 30px;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 4px;
}

.question-result {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.question-text {
  margin: 10px 0;
  font-style: italic;
}

.answer-comparison {
  margin-top: 15px;
}

.user-answer, .correct-answer, .points-earned {
  margin: 8px 0;
}

.correct {
  color: #27ae60;
  font-weight: bold;
}

.incorrect {
  color: #e74c3c;
  font-weight: bold;
}

.partial-credit {
  color: #f39c12;
  font-style: italic;
}

.restart-btn {
  margin-top: 30px;
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1em;
}

.blank-space {
  display: inline-block;
  min-width: 150px;
  border-bottom: 1px solid #333;
  margin: 0 5px;
}

.error {
  color: #e74c3c;
  padding: 15px;
  background: #fdecea;
  border-radius: 4px;
}
</style>