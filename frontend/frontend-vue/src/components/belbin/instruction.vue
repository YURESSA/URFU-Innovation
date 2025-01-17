<template>
  <div class="instruction__wrapper">
    <div class="relative__wrapper">
      <button class="close-instruction" @click="emit('closeInstruction')"><img src="@public/assets/main-page/cross-circle-svgrepo-com.svg" alt=""></button>
      <div class="instryction">
        <h4>Инструкция</h4>
        <p>
          В каждой из семи частей данного теста распределите <b>10</b> баллов между <b>8</b> утверждениями. <br>
          Если вы согласны с каким-либо утверждением на все <b>100%</b>, вы можете отдать ему все <b>10</b> баллов.
        </p>
        <p>
          Рекомендуем распределять баллы <b>5/3/2</b> для достоверности результата. <br>
          По результатам прохождения теста будет определена <b>ваша роль</b> в команде.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue';

const emit = defineEmits(['closeInstruction'])
</script>

<style scoped>
.instruction__wrapper{
  position: fixed;
  display: flex;
  justify-content: center;
  align-items: center;

  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 10;

  background-color: rgba(0, 0, 0, 0.8);
}

.instryction{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 25px;
  padding: 60px 60px;

  background-color: whitesmoke;
  border-radius: 14px;
}

.relative__wrapper{
  position: relative;
}

.close-instruction{
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 0;
  background-color: whitesmoke;
  border: none;
  border-radius: 5px;
}

.close-instruction:hover{
  background-color: rgba(192, 192, 192, 0.623);
}

.close-instruction:active{
  background-color: rgba(146, 146, 146, 0.623);
}

@media screen and (max-width: 980px) {
  .instryction{
    padding: 30px 30px;
    max-width: 300px;
  }
  .close-instruction{
    top: 10px;
    right: 10px;
  }
}
</style>