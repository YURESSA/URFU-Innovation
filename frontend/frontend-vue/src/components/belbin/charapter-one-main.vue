<template>
  <main>
    <div class="test-form">
      <div class="charapter">
        <h4><span @click="plus()">{{ charapter }}</span> раздел из 7</h4>
      </div>
      <div class="question">
        <h4>{{ test.questions[charapter - 1].block_name }}</h4>
      </div>
      <div class="form">
        <form ref="testForm" method="post" v-for="(item, i) in test.questions[charapter - 1].questions">
          <p>{{ i+1 }}. {{ item }}</p>
          <div class="slider-container">
            <input type="range" min="0" :max="max" value="0" class="slider" @input="updateValue" v-model="value" />
            <div class="slider-labels">
              <span v-for="num in max + 1" :key="num" class="label">{{ num - 1 }}</span>
            </div>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';

const max = ref(10);
const charapter = ref(1);
const props = defineProps({
  test: Array
});

function plus() {
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

input{
  width: 100%;
}

.test-form{
  width: 50%;
}

main{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.charapter{
  margin-bottom: 30px;
}

.question h4{
  font-weight: 900;
}

.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 3px;
  background: #490707;
  outline: none;
  border-radius: 5px;
}

.slider-container {
  position: relative;
  width: 100%;
  margin-top: 20px;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  padding-left: 1.5%;
}

.label {
  font-size: 12px;
  color: #333;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: #57c0cf;
  border: 1px solid #2b2a28;
  cursor: pointer;
  border-radius: 50%;
  margin-top: -7px;
}

.slider::-webkit-slider-runnable-track {
  width: 100%;
  height: 3px;
  background: #a6a6a6;
  border-radius: 5px;
}
</style>