<template>
  <div class="profile-page" v-if="user">
    <div class="container">
      <header>
        <div class="header__wrapper">
          <div class="logo">
            <router-link to="/"><img src="@public/assets/main-page/logo.svg" alt=""></router-link>
          </div>
          <div class="title">
            <h2>Личный кабинет</h2>
          </div>
        </div>
      </header>

      <main class="profile-content">
        <section class="user-info">
          <div class="info-card">
            <h1 class="user-name">{{ user.full_name }}</h1>
            <div class="contact-grid">
              <div class="contact-item">
                <span class="label">Телефон</span>
                <a :href="'tel:' + user.phone_number" class="value">{{ user.phone_number }}</a>
              </div>
              <div class="contact-item">
                <span class="label">Telegram</span>
                <a :href="'https://t.me/' + user.telegram_id.replace('@', '')" target="_blank" class="value">{{ user.telegram_id }}</a>
              </div>
            </div>
          </div>
        </section>

        <section class="tests-section">
          <div class="section-header">
            <h2 class="section-title">Ваши результаты</h2>
            <div class="arrow-line"></div>
          </div>

          <div class="tests-grid" v-if="user.tests && user.tests.length">
            <div v-for="test in user.tests" :key="test.user_test_id" class="test-card">
              <div class="test-card__info">
                <span class="test-date">{{ formatDate(test.timestamp) }}</span>
                <h3 class="test-name">{{ test.test_name }}</h3>
              </div>
              <div class="test-card__action">
                <router-link 
                  :to="{ name: test.test_name === 'Тест DISC' ? 'DiscResult' : 'BelbinResult', params: { id: test.user_test_id }}" 
                  class="btn-view"
                >
                  Смотреть результат
                </router-link>
              </div>
            </div>
          </div>
          
          <div v-else class="empty-state">
            <p>Вы еще не прошли ни одного теста.</p>
            <router-link to="/tests" class="btn-primary">Найти тесты</router-link>
          </div>
        </section>
      </main>
    </div>
  </div>
  <div v-else class="loading-state">Загрузка профиля...</div>
</template>

<script setup>
import { useDataStore } from '@/stores/store';
import { computed, onMounted } from 'vue';

const store = useDataStore();

onMounted(() => {
  store.getUserTestData();
});

const user = computed(() => store.getUser);

// Форматирование даты в привычный вид: 29.04.2026
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
};
</script>

<style scoped>
.profile-page {
  background-color: #eee5e5;
  min-height: 100vh;
  padding: 40px 20px;
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

/* User Info */
.user-info {
  margin-bottom: 50px;
}

.info-card {
  background: #fff;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

.user-name {
  font-size: 48px;
  font-weight: 900;
  margin-bottom: 25px;
  color: #1a1a1a;
}

.contact-grid {
  display: flex;
  gap: 40px;
}

.contact-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 14px;
  text-transform: uppercase;
  color: #888;
  letter-spacing: 1px;
  margin-bottom: 5px;
}

.value {
  font-size: 20px;
  font-weight: 700;
  color: #333;
  text-decoration: none;
}

.value:hover { color: #57c0cf; }

/* Tests List */
.section-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.section-title {
  font-size: 24px;
  font-weight: 900;
  text-transform: uppercase;
  white-space: nowrap;
}

.arrow-line {
  height: 2px;
  background: #333;
  width: 100%;
  position: relative;
}

.arrow-line::after {
  content: '';
  position: absolute;
  right: 0;
  top: -4px;
  width: 10px;
  height: 10px;
  border-top: 2px solid #333;
  border-right: 2px solid #333;
  transform: rotate(45deg);
}

.tests-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.test-card {
  background: rgba(255, 255, 255, 0.6);
  padding: 25px 30px;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.2s, background 0.2s;
}

.test-card:hover {
  background: #fff;
  transform: translateX(10px);
}

.test-date {
  font-size: 14px;
  color: #57c0cf;
  font-weight: 700;
}

.test-name {
  font-size: 22px;
  font-weight: 800;
  margin: 5px 0 0 0;
}

.btn-view {
  padding: 10px 25px;
  background: #1a1a1a;
  color: #fff;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 700;
  font-size: 14px;
  transition: background 0.3s;
}

.btn-view:hover {
  background: #57c0cf;
}

@media (max-width: 768px) {
  .user-name { font-size: 32px; }
  .contact-grid { flex-direction: column; gap: 20px; }
  .test-card { flex-direction: column; align-items: flex-start; gap: 15px; }
  .header__wrapper { flex-direction: column; align-items: flex-start; }
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