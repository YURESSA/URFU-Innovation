<template>
  <footer>
    <div class="footer__wrapper">
      <div class="remained">
        <h5>Осталось {{ remainingPoints }} из 10 баллов</h5>
      </div>
      <button v-if="charapter != 7" @click="nextCharapter(charapter)" :disabled="isNextDisabled">Далее</button>
      <button v-if="charapter == 7" @click="submitData" :disabled="isNextDisabled">Отправить</button>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useDataStore } from '@/stores/store.js';

const router = useRouter();
const store = useDataStore();

const props = defineProps({
  remainingPoints: Number,
  sliderValues: Array,
  charapter: Number
});

console.log(props.remainingPoints)
const isNextDisabled = computed(() => props.remainingPoints != 0)

const result = {'1section1': 1, '1section2': 2, '1section3': 0, '1section4': 2, '1section5': 1, '1section6': 2, '1section7': 1, '1section8': 1, '2section1': 1, '2section2': 1, '2section3': 1, '2section4': 1, '2section5': 2, '2section6': 0, '2section7': 2, '2section8': 2, '3section1': 1, '3section2': 1, '3section3': 3, '3section4': 1, '3section5': 1, '3section6': 0, '3section7': 1, '3section8': 2, '4section1': 1, '4section2': 0, '4section3': 2, '4section4': 2, '4section5': 1, '4section6': 3, '4section7': 1, '4section8': 0, '5section1': 0, '5section2': 1, '5section3': 2, '5section4': 0, '5section5': 2, '5section6': 0, '5section7': 3, '5section8': 2, '6section1': 2, '6section2': 0, '6section3': 2, '6section4': 1, '6section5': 1, '6section6': 2, '6section7': 1, '6section8': 1, '7section1': 2, '7section2': 1, '7section3': 2, '7section4': 1, '7section5': 1, '7section6': 1, '7section7': 0, '7section8': 2}

const emit = defineEmits(['incrementCharapter']);

function nextCharapter() {
  emit('incrementCharapter');
}

const submitData = async () => {
  try {
    await store.fetchBelbinResult(result)
    console.log('Ответ от сервера:', store.getBelbinResult);
    router.push('/belbin-result');
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
    if (error.response) {
      console.error('Ответ сервера с ошибкой:', error.response.data);
    }
  }
};
</script>

<style scoped>
footer{
  display: flex;
  justify-content: center;
}

button{
  border: 0.50px solid #2b2a28;
  border-radius: 7px;
  width: 20%;
  height: 100%;
  background-color: #a6a6a6;
}

.footer__wrapper{
  width: 50%;
  display: flex;
  justify-content: space-between;
}
</style>