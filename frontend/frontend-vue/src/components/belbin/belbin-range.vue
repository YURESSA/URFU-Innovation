<template>
  <p>{{ index+1 }}. {{ question }}</p>
  <div class="slider-container">
    <input
      type="range"
      class="slider"
      :min="min"
      :max="max"
      v-model="dataV"
      @input="onInput"
    />
    {{ dataV }}
    <div class="slider-labels">
      <span v-for="num in 11" :key="num" class="label">{{ num - 1 }}</span>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref, defineEmits, watch } from 'vue';

const emit = defineEmits(['update:value', 'updateRemained'])

const props = defineProps({
  max: Number,
  min: Number,
  limit: {
    type: Number,
    default: 10,
  },
  value: Number,
  question: String,
  index: Number,
})

const dataV = ref(props.value || 0)

watch(
  () => props.value,
  (newValue) => {
    dataV.value = newValue;
    emit('updateRemained')
  }
);

function onInput(e){
  const current = Number(e.target.value);
  if (current <= props.limit) {
    dataV.value = current;
  } else{
    dataV.value = props.limit
  }
  emit('update:value', dataV.value)
  emit('updateRemained')
}

</script>

<style scoped>
.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 3px;
  background: #490707;
  outline: none;
  border-radius: 5px;
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

.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  padding-left: 1%;
}

.label {
  font-size: 12px;
  color: #333;
}
</style>