<template>
  <div class="page__wrapper" v-if="isLoading">
    <chapter-one-header v-if="chapter == 1" :chapter="chapter"></chapter-one-header>
    <belbin-header v-if="chapter != 1" :chapter="chapter"></belbin-header>
    <test-belbin 
      class="main" 
      :chapter="chapter" 
      :test="test" 
      :remainedPoints="remainedPoints"
      :currentValue="currentValue"
      @updateRemained="updateRemained"
      @updateResult="updateResult"
    ></test-belbin>
    <belbin-footer :chapter="chapter" :remainedPoints="remainedPoints" :result="result" @updateResult="updateResult" @incrementchapter="chapter++"></belbin-footer>
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


onMounted(async () => {
  await store.fetchBelbin();
  isLoading.value = true;
});

const test = computed(() => store.getBelbin);
const chapter = ref(1);
const remainedPoints = ref(10);
const result = [];

const currentValue = ref([
  {
    points: ref(0),
  },
  {
    points: ref(0),
  },
  {
    points: ref(0),
  },
  {
    points: ref(0),
  },
  {
    points: ref(0),
  },
  {
    points: ref(0),
  },
  {
    points: ref(0),
  },
  {
    points: ref(0),
  },
]);

const updateRemained = (newPoint) =>{
  remainedPoints.value = newPoint;
}

const updateResult = () =>{
  let chapterResult = [];
  currentValue.value.forEach((e) => {
    chapterResult.push(e.points)
  });
  result.push(chapterResult)
  currentValue.value.forEach((e) => {
    e.points = 0
  });
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