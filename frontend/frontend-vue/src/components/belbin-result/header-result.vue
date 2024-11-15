<template>
  <header>
    <div class="header__wrapper">
      <div class="logo">
        <img src="/src/assets/main-page/логотип ИИ 1.svg" alt="">
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
}

.title{
  width: 40%;
}
</style>