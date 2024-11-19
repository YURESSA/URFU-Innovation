<template>
  <header>
    <h4><span @click="plus()">{{ charapter }}</span> раздел из 7</h4>
  </header>
</template>

<script setup>
import { ref } from 'vue';
let charapter = ref(1)

function plus(){
  charapter.value += 1
}
</script>

<style scoped>
span{
  font-family: inherit;
  font-size: inherit;
  font-weight: inherit;
  color: #57c0cf;
}
</style>