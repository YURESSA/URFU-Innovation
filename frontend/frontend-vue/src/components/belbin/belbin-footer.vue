<template>
  <footer>
    <div class="footer__wrapper">
      <div class="remained">
        <h5>Осталось {{ remainedPoints }} из 10 баллов</h5>
      </div>
      <button v-if="chapter != 7" @click="nextchapter(chapter)" :disabled="isNextDisabled">Далее</button>
      <button v-if="chapter == 7" @click="submitData" :disabled="isNextDisabled">Отправить</button>
    </div>
  </footer>
</template>

<script setup>
import { computed, defineEmits } from 'vue';
import { useRouter } from 'vue-router';
import { useDataStore } from '@/stores/store.js';

const router = useRouter();
const store = useDataStore();

const props = defineProps({
  remainedPoints: Number,
  chapter: Number,
  result: Array
});

const isNextDisabled = computed(() => props.remainedPoints != 0)


const emit = defineEmits(['incrementchapter', 'updateResult']);

function nextchapter() {
  emit('incrementchapter');
  emit('updateResult')
}

const submitData = async () => {
  emit('updateResult')
  try {
    await store.fetchBelbinResult(props.result)
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
  background-color: #57C0CF;
  justify-content: center;
  color: black;
}

button:hover{
  background-color: #7EEBFB
}

button:disabled{
  background-color: #A6A6A6;
  color: black;
}

.footer__wrapper{
  width: 50%;
  display: flex;
  justify-content: space-between;
}

@media screen and (max-width: 980px) {
  .footer__wrapper{
    width: 75%;
    align-items: center;
  }
  button{
    width: 30%;
    height: 35px;
  }
  h5{
    font-size: 18px;
  }
}
</style>