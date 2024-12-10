<template>
  <header>
    <div class="header__wrapper">
      <div class="logo">
        <router-link to="/"><img src="/src/assets/main-page/логотип ИИ 1.svg" alt=""></router-link>
      </div>
      <div class="title">
        <h2>Результат теста</h2>
      </div>
    </div>
  </header>
</template>

<script setup>

</script>

<style scoped>
header{
  display: flex;
  justify-content: center;
  height: 150px;
}

.header__wrapper{
  width: 50%;
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

@media screen and (max-width: 980px) {
  .header__wrapper{
    width: 85%;
    flex-direction: column;
    align-items: flex-start;
    padding-top: 40px;
  }
  img{
    width: 70px;
    height: 40px;
  }
}
</style>