<template>
  <main>
    <div class="title">
      <h4 class="font">Ваши сильные роли</h4>
      <img src="/src/assets/belbin/Arrow 1.svg" alt="">
    </div>
    <div class="top-roles">
      <div class="role" v-for="(item, i) in data" :key="i">
        <div class="name">
          <h5 class="second">{{ item.role }}</h5>
        </div>
        <p>{{ item.description }}</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  data: Array,
})
</script>

<style scoped>
main{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 65%;
  margin: 0 auto;
}

.title{
  display: flex;
  align-items: center;
  margin-bottom: 45px;
  margin-top: 70px;
  gap: 30px;
}

.title img{
  padding-top: 20px;
}

.font{
  text-align: center;
  font-weight: 900;
}

.second{
  color: #57c0cf;
}

.top-roles{
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 80%;
}

.role{
  display: flex;
  gap: 60px;
}

.role .name{
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  min-width: 300px;
}

.role p{
  max-width: 417px;
  min-height: 190px;
}

</style>