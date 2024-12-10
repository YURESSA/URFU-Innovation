<template>
  <div class="page__wrapper">
    <login />
  </div>
</template>

<script setup>
import login from '@/components/admin/login.vue';
</script>

<style scoped>
.page__wrapper{
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 100vw;
  min-height: 100vh;
  background-color: rgb(0, 77, 77);
}
</style>