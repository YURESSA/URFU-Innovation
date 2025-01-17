<template>
  <header>
    <div class="header__wrapper">
      <div class="logo">
        <img src="@public/assets/main-page/logo.svg" alt="">
      </div>
      <div class="chapter">
        <h4><span>{{ chapter }}</span> раздел из 7</h4>
      </div>
      <button @click="emit('openInstruction')">Инструкция</button>
    </div>
  </header>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  chapter: Number
});

const emit = defineEmits(['openInstruction'])
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
  flex-wrap: wrap;
  padding-top: 40px;
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
  color: black;
  justify-content: center;
  margin-bottom: -25px;
}

button:hover{
  background-color: #7EEBFB;
}

@media screen and (max-width: 980px) {
  .header__wrapper{
    width: 75%;
  }
  .chapter{
    order: 1;
  }
  button{
    width: 50%;
  }
  .logo > img{
    width: 70px;
    height: 40px;
    margin-bottom: -25px;
  }
}
</style>