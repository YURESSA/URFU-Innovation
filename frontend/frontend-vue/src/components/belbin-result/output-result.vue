<template>
  <main>
    <div class="title">
      <h4 class="font">Ваши сильные роли</h4>
      <img src="/public/assets/belbin/Arrow 1.svg" alt="">
    </div>
    <div class="top-roles">
      <div class="role" v-for="(item, i) in data.prefer_roles" :key="i">
        <div class="name">
          <h5 class="second">{{ item.role }}</h5>
          <img :src="`/static/assets/belbin-result/${item.file_name}`" alt="">
        </div>
        <div class="info-role">
          <h5>Описание</h5>
          <p class="start-descript">
            Термин, который характеризует — <b>{{ item.term }}</b> <br>
            {{ item.goal }}
          </p>
          <p>{{ item.description }}</p>
          <h5>Сильные стороны</h5>
          <ul>
            <li v-for="(strong, i) in item.strong_side" :key="i"> {{ strong }} </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="title weak-title">
      <h4 class="font">Ваши слабые роли</h4>
      <img src="/public/assets/belbin/Arrow 1.svg" alt="">
    </div>
    <div class="non-top-roles">
      <div class="role" v-for="(item, i) in data.un_prefer_roles" :key="i">
        <div class="name">
          <h5 class="second">{{ item.role }}</h5>
          <img :src="`/static/assets/belbin-result/${item.file_name}`" alt="">
        </div>
        <div class="info-role">
          <h5>Описание</h5>
          <p class="start-descript">
            Термин, который характеризует — <b>{{ item.term }}</b> <br>
            {{ item.goal }}
          </p>
          
          <p>{{ item.description }}</p>
          <h5>Слабые стороны</h5>
          <ul>
            <li v-for="(weak, i) in item.weak_side" :key="i"> {{ weak }} </li>
          </ul>
          <h5>Рекомендации для развития</h5>
          <ul>
            <li v-for="(recomend, i) in item.recommendations" :key="i"> {{ recomend }} </li>
          </ul>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  data: Object,
})

console.log(props.data.prefer_roles[0].strong_side)
</script>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 65%;
  margin: 0 auto;
}

.start-descript{
  margin-bottom: 0px;
}

.title {
  display: flex;
  align-items: center;
  margin-bottom: 45px;
  margin-top: 70px;
  gap: 30px;
}

.weak-title{
  margin-top: 200px;
}

.title img {
  padding-top: 20px;
}

.font {
  text-align: center;
  font-weight: 900;
}

.second {
  color: #57c0cf;
}

.top-roles, .non-top-roles {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 80%;
  gap: 100px;
}

.role {
  display: flex;
  gap: 60px;
}

.name {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 20px;
}

.name > img {
  width: 250px;
  height: 300px;
}

.role .name {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  min-width: 300px;
}

.role p {
  max-width: 417px;
  /* min-height: 190px; */
}

li {
  max-width: 417px;
}

.info-role {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-role > h5 {
  font-weight: 600;
  font-size: 30px;
}

h4 {
  width: max-content;
}

@media screen and (max-width: 980px) {
  main {
    width: 100%;
  }

  h4 {
    font-size: 32px;
  }

  .title > img {
    display: none;
  }

  .role {
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }
}
</style>