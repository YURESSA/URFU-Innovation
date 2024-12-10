<template>
  <h4>Диаграмма с процентным соотношением ролей</h4>
  <div id="chart">
    <apexchart class="vue-chart" type="radar" height="350" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<script setup>
import { ref, defineProps, computed } from 'vue'

const props = defineProps({
  result: Object
})

const roles = props.result.map(item => item.name);
const percentages = props.result.map(item => item.pl); 
const mq = ref(window.matchMedia('(max-width: 980px)'))
const radarSize = computed(() =>{
  if(mq.value.matches){
    return 100
  } else {
    return 140
  }
})

const series = ref([
  {
    name: 'Процент',
    data: percentages
  }
])

const chartOptions = ref({
  chart: {
    height: 350,
    type: 'radar',
  },
  dataLabels: {
    enabled: true
  },
  plotOptions: {
    radar: {
      size: radarSize,
      polygons: {
        strokeColors: '#e9e9e9',
        fill: {
          colors: ['#f8f8f8', '#fff']
        }
      }
    }
  },
  colors: ['#FF4560'],
  markers: {
    size: 8,
    colors: ['#fff'],
    strokeColor: '#FF4560',
    strokeWidth: 4,
  },
  tooltip: {
    y: {
      formatter: (val) => val
    }
  },
  xaxis: {
    categories: roles
  },
  yaxis: {
    labels: {
      formatter: (val, i) => (i % 2 === 0 ? val : '')
    }
  }
})
</script>

<style scoped>
h4 {
  text-align: center;
  margin-top: 40px;
}
</style>
