<template>
  <header>
    <div class="header__wrapper">
      <div class="title">
        <h1>Тест <br> Белбина</h1>
      </div>
      <div class="logo">
        <img src="@public/assets/belbin/line1.svg" class="line1" alt="">
        <img src="@public/assets/main-page/logo.svg" class="urfu" alt="">
        <img src="@public/assets/belbin/line2.svg" class="line2" alt="">
      </div>
    </div>
    <div class="description">
      <h4 class="slogan">определи свою роль в команде!</h4>
      <p>В каждой из семи частей данного теста распределите <b>10</b> баллов между <b>8</b> утверждениями. <br>
        Если вы согласны с каким-либо утверждением на все <b>100%</b>, вы можете отдать ему все <b>10</b> баллов.</p>
      <p>Рекомендуем распределять баллы <b>5/3/2</b> для достоверности результата.
        По результатам прохождения теста будет определена <b>ваша роль</b> в команде.</p>
    </div>
    <div class="charapter">
      <h4><span>{{ chapter }}</span> раздел из 7</h4>
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
  width: max-content;
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

main{
  display: flex;
  justify-content: center;
  width: 100vw;
}

.description{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 50%;
  margin: 30px 0;
}

.slogan{
  color: #57c0cf;
  text-transform: uppercase;
}

.charapter{
  margin-bottom: 30px;
  width: 50%;
}

span{
  font-family: inherit;
  font-size: inherit;
  font-weight: inherit;
  color: #57c0cf;
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
    left: 180px;
  }
  .line2{
    width: 100px;
    height: 85px;
    top: 15px;
    left: 250px;
  }
  .urfu{
    width: 70px;
    height: 40px;
    top: -60px;
    left: 280px;
  }
  h4{
    font-size: 24px;
  }
  .description, .charapter{
    width: 75%;
  }
}
</style>