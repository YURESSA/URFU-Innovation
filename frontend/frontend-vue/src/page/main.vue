<template>
  <div class="page__wrapper">
    <header>
      <div class="header__wrapper">
        <div class="title">
          <h1>Тесты</h1>
          <h2>предпринимательских <br> компетенций</h2>
        </div>
        <div class="logo">
          <img src="../assets/main-page/элемент-линии.svg" class="line" alt="" />
          <img src="../assets/main-page/логотип ИИ 1.svg" class="urfu" alt="инновационная инфраструктура УрФУ"/>
        </div>
      </div>
    </header>
    <main>
      <div v-for="(item, i) in tests" :key="i">
        <test-priview :title="item.test_title" @click="openForm(item.test_url)"></test-priview>
      </div>
      <student-form
        v-if="isFormVisible"
        :test-url="selectedTestUrl" @closeForm="closeForm"></student-form>
    </main>
  </div>
</template>

<script setup>
import { computed, ref} from 'vue';
import { useDataStore } from '@/stores/store.js';
import StudentForm from '@/components/main/student-form.vue';
import TestPriview from '@/components/main/test-priview.vue'

const isFormVisible = ref(false);
const selectedTestUrl = ref('');
const store = useDataStore();
const tests = computed(() => store.getTests);

function openForm(testUrl) {
  isFormVisible.value = true;
  selectedTestUrl.value = testUrl;
  document.body.classList.add('modal-open');
}

function closeForm() {
  isFormVisible.value = false;
  selectedTestUrl.value = '';
  document.body.classList.remove('modal-open');
}

</script>

<style scoped>
.page__wrapper{
  min-height: 100vh;
  width: 100%;
  background: rgb(80, 188, 190);
  background: linear-gradient(30deg, rgba(80, 188, 190, 1) 0%, rgba(164, 215, 215, 1) 75%, rgba(236, 237, 237, 1) 100%);
}

header{
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 80px;
  margin-bottom: 35px;
}

.header__wrapper {
  display: flex;
  align-items: center;
}

.logo {
  position: relative;
  left: 10px;
  top: -50px;
}

.line{
  position: absolute;
  top: -140px;
}

.urfu{
  position: absolute;
  right: -320px;
  top: -30px;
}

h2{
  max-width: 679px;
}

main{
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.modal-open{
  overflow-y: hidden;
}

@media screen and (max-width: 980px) {
  header{
    padding-top: 150px;
  }
  .header__wrapper {
    flex-direction: column-reverse;
  }
  .logo{
    left: 0px;
    top: 0px;
  }
  .line{
    width: 120px;
    height: 110px;
  }
  .urfu{
    position: absolute;
    right: -175px;
    top: -80px;
    width: 90px;
    height: 50px;
  }
}

</style>