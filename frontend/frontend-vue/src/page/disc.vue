<template>
  <div class="test-page" v-if="testData">
    <div class="container">
      <header>
        <div class="header__wrapper">
          <div class="title">
            <h1>Тест <br> DISC</h1>
          </div>
          <div class="logo">
            <img src="@public/assets/belbin/line1.svg" class="line1" alt="">
            <a href="/"><img src="@public/assets/main-page/logo.svg" class="urfu" alt=""></a>
            <img src="@public/assets/belbin/line2.svg" class="line2" alt="">
          </div>
        </div>
        <div class="description">
          <h4 class="slogan">ОПРЕДЕЛИ СВОЙ ТИП ЛИЧНОСТИ!</h4>
          <p>Внимательно прочитайте вопрос и выберите <b>один</b> вариант ответа, который наиболее точно описывает ваше поведение или предпочтения.</p>
        </div>
      </header>

      <main class="test-main">
        <div class="progress-info">
          <span class="current-step">{{ currentQuestionIndex + 1 }}</span>
          <span class="total-steps"> раздел из {{ testData.questions.length }}</span>
        </div>

        <section class="question-section" v-if="currentQuestion">
          <h2 class="question-text">{{ currentQuestion.text }}</h2>

          <div class="options-list">
            <label 
              v-for="(text, key) in currentQuestion.options" 
              :key="key" 
              class="option-item"
              :class="{ 'is-selected': answers[currentQuestion.id] === key }"
            >
              <input 
                type="radio" 
                :name="'question-' + currentQuestion.id" 
                :value="key"
                v-model="answers[currentQuestion.id]"
                class="hidden-radio"
              />
              <div class="custom-radio"></div>
              <span class="option-text">{{ text }}</span>
            </label>
          </div>
        </section>

        <footer class="test-navigation">
          <button 
            @click="prevQuestion" 
            :disabled="currentQuestionIndex === 0"
            class="btn-secondary"
          >
            Назад
          </button>
          
          <button 
            v-if="currentQuestionIndex < testData.questions.length - 1"
            @click="nextQuestion" 
            :disabled="!answers[currentQuestion.id]"
            class="btn-primary"
          >
            Далее
          </button>

          <button 
            v-else 
            @click="submitTest" 
            :disabled="!answers[currentQuestion.id]"
            class="btn-submit"
          >
            Завершить тест
          </button>
        </footer>
      </main>
    </div>
  </div>
  <div v-else class="loading">Загрузка данных теста...</div>
</template>

<script setup>
import { useDataStore } from '@/stores/store';
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const store = useDataStore();
const router = useRouter();

const currentQuestionIndex = ref(0);
const answers = ref({}); // Храним ответы в формате { id_вопроса: 'A' }

onMounted(() => {
  store.fetchDisc();
});

const testData = computed(() => store.getDisc);
const currentQuestion = computed(() => testData.value?.questions[currentQuestionIndex.value]);

function nextQuestion() {
  if (currentQuestionIndex.value < testData.value.questions.length - 1) {
    currentQuestionIndex.value++;
    // window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

function prevQuestion() {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--;
  }
}

async function submitTest() {
  const resultData = {
    answers: Object.entries(answers.value).map(([id, value]) => ({
      question_id: parseInt(id),
      answer: value
    }))
  };
  console.log(resultData)

  try {
    await store.fetchDiscResult(resultData);
    router.push('/disc-result');
  } catch (error) {
    console.error("Ошибка при отправке теста", error);
  }
}
</script>

<style scoped>
.test-page {
  background-color: #eee5e5;
  min-height: 100vh;
  color: #333;
  padding: 40px 20px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

.header__wrapper{
  display: flex;
  justify-content: center;
  padding-top: 45px;
}

header{
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title{
  width: 400px;
}

.logo{
  position: relative;
  width: 350px;
}

.line1{
  position: absolute;
  top: 0px;
}

.line2{
  position: absolute;
  bottom: -10px;
  left: 125px;
}

.urfu{
  position: absolute;
  top: 30px;
  left: 180px;
}

.description{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  margin: 30px 0;
}

.description > p {
  font-size: 20px;
}

.slogan{
  color: #57c0cf;
  text-transform: uppercase;
}

.charapter{
  margin-bottom: 30px;
  width: 50%;
}

/* Progress */
.progress-info {
  font-size: 28px;
  margin-bottom: 20px;
}

.current-step {
  color: #57c0cf;
  font-weight: bold;
  font-size: 36px;
}

.question-text {
  font-size: 32px;
  font-weight: 800;
  margin-bottom: 30px;
  line-height: 1.2;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
}

.option-item:hover {
  background: rgba(255, 255, 255, 0.8);
}

.option-item.is-selected {
  border-color: #57c0cf;
  background: white;
}

.hidden-radio {
  display: none;
}

.custom-radio {
  width: 20px;
  height: 20px;
  border: 2px solid #57c0cf;
  border-radius: 50%;
  margin-right: 15px;
  position: relative;
  flex-shrink: 0;
}

.option-item.is-selected .custom-radio::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translateX(-50%) translateY(-50%);
  width: 10px;
  height: 10px;
  background-color: #57c0cf;
  border-radius: 50%;
}

.option-text {
  font-size: 18px;
  line-height: 1.4;
}

.test-navigation {
  margin-top: 50px;
  display: flex;
  gap: 20px;
  padding-bottom: 100px;
}

button {
  padding: 12px 30px;
  border-radius: 5px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  border: none;
  transition: opacity 0.2s;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary, .btn-submit {
  background-color: #57c0cf;
  color: white;
}

.btn-secondary {
  background-color: transparent;
  border: 2px solid #57c0cf;
  color: #57c0cf;
}

@media (max-width: 768px) {
  .main-title, .sub-title {
    font-size: 40px;
  }
  .urfu-logo {
    width: 80px;
  }
}

@media screen and (max-width: 980px) {
  .header__wrapper{
    flex-direction: column-reverse;
    align-items: center;
    padding-top: 110px;
  }
  .line1{
    width: 95px;
    height: 140px;
    top: -80px;
    left: 150px;
  }
  .line2{
    width: 100px;
    height: 85px;
    top: 15px;
    left: 220px;
  }
  .urfu{
    width: 97px;
    top: -60px;
    left: 242px;
  }
  .title {
    width: 90%;
  }
  h4{
    font-size: 24px;
  }
  .description {
    width: 100%;
  }
}
</style>