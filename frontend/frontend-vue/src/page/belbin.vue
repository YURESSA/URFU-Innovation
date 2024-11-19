<template>
  <div class="page__wrapper" v-if="isLoading">
    <chapter-one-header v-if="charapter == 1" :charapter="charapter"></chapter-one-header>
    <belbin-header v-if="charapter != 1" :charapter="charapter"></belbin-header>
    <test-belbin 
      class="main" 
      :charapter="charapter" 
      :test="test" 
      @updateRemainingPoints="updateRemainingPoints"
      @updateSliderValues="updateSliderValues"
    ></test-belbin>
    <belbin-footer :charapter="charapter" :remainingPoints="remainingPoints" :sliderValues="sliderValues" @incrementCharapter="charapter++"></belbin-footer> <!-- Передаем sliderValues в belbin-footer -->
  </div>
  <div v-else>
    Загрузка...
  </div>
</template>

<script setup>
import { useDataStore } from '@/stores/store.js';
import { computed, ref, onMounted } from 'vue';
import ChapterOneHeader from '@/components/belbin/chapter-one-header.vue';
import TestBelbin from '@/components/belbin/test-belbin.vue';
import BelbinFooter from '@/components/belbin/belbin-footer.vue';
import BelbinHeader from '@/components/belbin/belbin-header.vue';

const store = useDataStore();
const isLoading = ref(false);
const remainingPoints = ref(10); // начальное количество оставшихся баллов
const sliderValues = ref([]); // создаем переменную для хранения значений слайдеров

onMounted(async () => {
  await store.fetchBelbin();
  isLoading.value = true;
});

const test = computed(() => store.getBelbin);
const charapter = ref(1);

function updateRemainingPoints(value) {
  remainingPoints.value = value; // обновляем оставшиеся баллы
}

function updateSliderValues(values) {
  sliderValues.value = values; // обновляем значения слайдеров
}
</script>

<style scoped>
.page__wrapper{
  min-height: 100vh;
  width: 100vw;
  background-color: #eee5e5;
  padding-bottom: 50px;
}

.main{
  margin-bottom: 40px;
}
</style>