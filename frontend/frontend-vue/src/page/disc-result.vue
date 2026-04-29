<template>
  <div class="results-page" v-if="data">
    <div class="container">
      <header>
        <div class="header__wrapper">
          <div class="logo">
            <router-link to="/"><img src="@public/assets/main-page/logo.svg" alt=""></router-link>
          </div>
          <div class="title">
            <h2>Результат теста</h2>
          </div>
        </div>
      </header>

      <main class="results-content">
        <section class="scores-section">
          <h2 class="section-title">Распределение компетенций</h2>
          <div class="scores-grid">
            <div v-for="item in sortedScores" :key="item.letter" class="score-card">
              <div class="score-letter">{{ item.letter }}</div>
              <div class="score-bar-wrapper">
                <div 
                  class="score-bar-fill" 
                  :style="{ width: (item.value / 15 * 100) + '%' }"
                ></div>
              </div>
              <div class="score-value">{{ item.value }}</div>
            </div>
          </div>
        </section>

        <section class="recommendations-section">
          <h2 class="section-title">Персональные рекомендации</h2>
          
          <div v-for="(rec, index) in data.recommendations" :key="index" class="rec-block">
            <div class="rec-header">
              <div class="rec-letter-badge">{{ rec.letter }}</div>
              <h3 class="rec-title">{{ rec.title }}</h3>
            </div>
            
            <ul class="rec-list">
              <li v-for="(item, i) in rec.items" :key="i" class="rec-item">
                <span class="bullet"></span>
                <p>{{ item }}</p>
              </li>
            </ul>
          </div>
        </section>

        <section class="contact-section">
          <p class="p__bold">
            Личная консультация и ответы на вопросы по диагностике – Беспамятных Елена Владимировна, 
            <a href="tel:+79022701569">+79022701569</a>
          </p>
        </section>

        <footer class="results-footer">
          <router-link to="/profile" class="btn-back">Вернуться в профиль</router-link>
        </footer>
      </main>
    </div>
  </div>
  <div v-else class="loading-state">
    Загрузка результатов...
  </div>
</template>

<script setup>
import { useDataStore } from '@/stores/store';
import { computed } from 'vue';

const sortedScores = computed(() => {
  if (!data.value || !data.value.scores) return [];
  
  const order = ['D', 'I', 'S', 'C'];
  
  // Возвращаем массив объектов [{ letter: 'D', value: 5 }, ...]
  return order.map(letter => ({
    letter,
    value: data.value.scores[letter] || 0
  }));
});

const store = useDataStore();
const data = computed(() => store.getDiscResult);
</script>

<style scoped>
.results-page {
  background-color: #eee5e5;
  min-height: 100vh;
  padding: 60px 20px;
  color: #333;
  font-family: 'PF Bulletin Sans Pro', sans-serif;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

/* Header */
header{
  display: flex;
  justify-content: center;
  height: 150px;
}

.header__wrapper{
  width: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.logo{
  width: 30%;
}

h2{
  height: 91px;
  line-height: 180%;
  min-width: max-content;
}

.title{
  width: 40%;
  text-align: center;
}

/* Scores */
.section-title {
  font-size: 28px;
  font-weight: 800;
  text-transform: uppercase;
  margin-bottom: 30px;
  border-bottom: 3px solid #333;
  display: inline-block;
}

.scores-section {
  margin-bottom: 60px;
}

.scores-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: rgba(255, 255, 255, 0.4);
  padding: 30px;
  border-radius: 12px;
}

.score-card {
  display: grid;
  grid-template-columns: 40px 1fr 40px;
  align-items: center;
  gap: 20px;
}

.score-letter {
  font-size: 24px;
  font-weight: 900;
  color: #57c0cf;
}

.score-bar-wrapper {
  height: 12px;
  background: #d1c7c7;
  border-radius: 6px;
  overflow: hidden;
}

.score-bar-fill {
  height: 100%;
  background-color: #57c0cf;
  transition: width 1s ease-out;
}

.score-value {
  font-size: 20px;
  font-weight: bold;
  text-align: right;
}

/* Recommendations */
.rec-block {
  margin-bottom: 40px;
  background: #fff;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.rec-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.rec-letter-badge {
  background: #57c0cf;
  color: white;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-size: 24px;
  font-weight: 900;
}

.rec-title {
  font-size: 22px;
  font-weight: 800;
  margin: 0;
}

.rec-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rec-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.bullet {
  width: 8px;
  height: 8px;
  background: #57c0cf;
  border-radius: 50%;
  margin-top: 8px;
  flex-shrink: 0;
}

.rec-item p {
  margin: 0;
  font-size: 16px;
  line-height: 1.5;
}

.contact-section {
  margin: 40px 0;
  padding: 25px;
  background: rgba(87, 192, 207, 0.1); /* Легкий оттенок бирюзового */
  border-left: 5px solid #57c0cf;
  border-radius: 8px;
}

.p__bold {
  font-weight: 800;
  font-size: 18px;
  line-height: 1.4;
  margin: 0;
}

.p__bold a {
  color: #57c0cf;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s;
}

.p__bold a:hover {
  border-color: #57c0cf;
}

/* Footer */
.results-footer {
  padding: 40px 0 100px;
  text-align: center;
}

.btn-back {
  display: inline-block;
  padding: 15px 40px;
  background: #333;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  transition: background 0.3s;
}

.btn-back:hover {
  background: #57c0cf;
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 24px;
  background: #eee5e5;
}

@media (max-width: 768px) {
  .main-title, .sub-title {
    font-size: 50px;
  }
  .contact-section {
    padding: 15px;
  }
  .rec-block {
    padding: 20px;
  }
}

@media screen and (max-width: 980px) {
  .header__wrapper{
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    padding-top: 40px;
  }
  img{
    width: 90px;
    /* height: 40px; */
  }
}
</style>