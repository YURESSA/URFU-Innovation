<template>
  <div class="test">
    <h2>{{ title }}</h2>
    <img src="/src/assets/main-page/star.svg" class="star" alt="Star" />
  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
</script>

<style scoped>
.test {
  display: flex;
  justify-content: left;
  align-items: center;
  background-color: #4dcac8;
  border: 1px solid #2b2a28;
  border-radius: 7px;
  width: 300px;
  height: 180px;
  padding: 27px 31px;
  position: relative;
}

.star {
  position: absolute;
  top: 0px;
  right: 0px;
}
</style>
