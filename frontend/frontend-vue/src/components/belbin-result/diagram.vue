<template>
  <h4>Диаграмма с процентным соотношением ролей</h4>
  <div id="chart">
    <apexchart type="radar" height="350" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<script setup>
// import { ref, defineProps } from 'vue'
// import { Chart, Responsive, Pie, Tooltip, Radar } from 'vue3-charts'


// const props = defineProps({
//   result: Object
// })


// const data = ref(props.result)
import { ref, defineProps } from 'vue'

const props = defineProps({
  result: Object
})

const roles = props.result.map(item => item.name);
const percentages = props.result.map(item => item.pl); 

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
      size: 140,
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
