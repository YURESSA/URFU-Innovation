<template>
  <header>
    <div class="header__wrapper">
      <div class="logo">
        <img src="/src/assets/main-page/логотип ИИ 1.svg" alt="">
      </div>
      <div class="chapter">
        <h4><span>{{ chapter }}</span> раздел из 7</h4>
      </div>
      <button @click="">Инструкция</button>
    </div>
  </header>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  chapter: Number
});
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
  justify-content: space-between;
  align-items: center;
}

h4{
  height: 87px;
  line-height: 300%;
}

span{
  font-family: inherit;
  font-size: inherit;
  font-weight: inherit;
  color: #57c0cf;
}

button{
  border: 0.50px solid #2b2a28;
  border-radius: 7px;
  width: 20%;
  height: 30%;
  background-color: #57c0cf;
  margin-top: 25px;
}
</style>