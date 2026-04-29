<template>
  <div class="admin-table">
    <div class="table-actions">
      <div class="date-filters">
        <div class="filter-item">
          <label>C:</label>
          <input type="date" v-model="filters.start_date" class="date-input">
        </div>
        <div class="filter-item">
          <label>По:</label>
          <input type="date" v-model="filters.end_date" class="date-input">
        </div>
      </div>

      <div class="buttons-group">
        <button class="btn-excel" @click="exportExcel">Скачать Excel</button>
        <button 
          class="btn-delete" 
          @click="confirmDelete" 
          :disabled="!filters.start_date || !filters.end_date"
        >
          Удалить за период
        </button>
      </div>
    </div>

    <DataTable 
      class="table" 
      removableSort 
      scrollable 
      scrollHeight="70vh" 
      :value="processedData" 
    >
      <Column field="full_name" sortable header="ФИО" style="min-width: 200px"></Column>

      <Column header="Контакты" style="min-width: 180px">
        <template #body="slotProps">
          <div class="contacts-cell">
            <a :href="`tel:${slotProps.data.phone_number}`" class="phone">{{ slotProps.data.phone_number }}</a>
            <a 
              v-if="slotProps.data.telegram_id"
              :href="`https://t.me/${slotProps.data.telegram_id.replace('@', '')}`" 
              target="_blank" 
              class="tg-link"
            >
              {{ slotProps.data.telegram_id }}
            </a>
          </div>
        </template>
      </Column>

      <Column header="Тест Белбина">
        <template #body="slotProps">
          <div v-if="slotProps.data.belbin" class="data-result">
            <div class="result-row" v-for="(val, key) in slotProps.data.belbin" :key="key">
              <span class="key">{{ key }}:</span>
              <span class="val">{{ val }}</span>
            </div>
          </div>
          <span v-else class="no-data">—</span>
        </template>
      </Column>

      <Column header="Тест DISC">
        <template #body="slotProps">
          <div v-if="slotProps.data.disc" class="data-result disc-results">
            <div class="result-row" v-for="(val, key) in slotProps.data.disc" :key="key">
              <span class="key">{{ key }}:</span>
              <span class="val">{{ val }}</span>
            </div>
          </div>
          <span v-else class="no-data">—</span>
        </template>
      </Column>

      <Column header="Даты прохождения" style="min-width: 250px">
        <template #body="slotProps">
          <div class="dates-list">
            <div 
              v-for="(test, idx) in slotProps.data.tests" 
              :key="idx" 
              class="date-row"
            >
              <span class="test-label">{{ test.test_name }}:</span>
              <span class="test-time">{{ formatDate(test.timestamp) }}</span>
            </div>
          </div>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { baseUrl, useDataStore } from '@/stores/store';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import axios from 'axios';

const props = defineProps({
  dataBase: Array,
})


const store = useDataStore();

const filters = ref({
  start_date: '',
  end_date: ''
});

const isLoading = ref(false);

// Превращаем массив пользователей с вложенными тестами в плоский формат для колонок
const processedData = computed(() => {
  return props.dataBase.map(user => {
    // Ищем конкретные тесты в массиве tests
    const belbinTest = user.tests.find(t => t.test_name === 'Тест Белбина');
    const discTest = user.tests.find(t => t.test_name === 'Тест DISC');

    return {
      ...user,
      belbin: belbinTest ? belbinTest.sections : null,
      disc: discTest ? discTest.sections : null,
      // Собираем все даты в один массив для отображения
      timestamps: user.tests.map(t => t.timestamp)
    };
  });
});

function formatDate(dateStr) {
  if (!dateStr) return '—';
  const date = new Date(dateStr);
  return date.toLocaleDateString('ru-RU', { 
    day: '2-digit', 
    month: '2-digit', 
    year: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function exportExcel() {
  axios.get(`${baseUrl}/user-tests/export`, {
    responseType: 'blob',
    withCredentials: true
  })
  .then(response => {
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a'); 
    link.href = url;
    link.setAttribute('download', 'test_results.xlsx');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  })
  .catch(error => console.error('Ошибка экспорта:', error));
}

// Функция удаления
async function deleteResults() {
  try {
    isLoading.value = true;
    
    // Отправляем DELETE запрос с параметрами
    const response = await axios.delete(`${baseUrl}/user-tests`, {
      params: {
        start_date: filters.value.start_date,
        end_date: filters.value.end_date,
        // test_name: 'DISC',
        // test_name: 'BELBIN'
      },
      withCredentials: true
    });

    if (response.data.success) {
      alert(`Успешно удалено записей: ${response.data.deleted_tests}`);
      await store.fetchDataBase();
    }
  } catch (error) {
    console.error('Ошибка при удалении:', error);
    alert('Ошибка при удалении данных. Проверь консоль.');
  } finally {
    isLoading.value = false;
  }
}

// Подтверждение действия
function confirmDelete() {
  const isConfirmed = confirm(
    `ВНИМАНИЕ! Вы собираетесь безвозвратно удалить все результаты тестов в период с ${filters.value.start_date} по ${filters.value.end_date}. Продолжить?`
  );
  
  if (isConfirmed) {
    deleteResults();
  }
}
</script>

<style scoped>
.admin-table {
  max-width: 95vw;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
}

.table {
  background: white;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* Стилизация ячеек с результатами */
.data-result {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
  min-width: 140px;
}

.disc-results {
  flex-direction: row; /* DISC можно в строчку, так как там короткие ключи */
  flex-wrap: wrap;
  gap: 8px;
}

.result-row {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #f0f0f0;
}

.key {
  color: #666;
}

.val {
  font-weight: 800;
  color: #0a4e4e;
}

/* Контакты и даты */
.contacts-cell, .dates-cell {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 14px;
}

.tg-link {
  color: #57c0cf;
  text-decoration: none;
  font-weight: bold;
}

.date-item {
  font-size: 12px;
  color: #888;
}

.no-data {
  color: #ccc;
  font-style: italic;
}

/* Кнопка */
.btn-excel {
  background: #1a1a1a;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.3s;
}

.btn-excel:hover {
  background: #57c0cf;
}

.dates-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.date-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
}

.test-label {
  font-weight: 700;
  color: #333;
  white-space: nowrap;
}

.test-time {
  color: #666;
  font-family: monospace; /* Моноширинный шрифт для дат всегда выглядит ровнее */
}

.table-actions {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  background: white;
  padding: 20px;
  border-radius: 12px;
  gap: 20px;
}

.date-filters {
  display: flex;
  gap: 15px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.date-input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
}

.buttons-group {
  display: flex;
  gap: 10px;
}

.btn-delete {
  background: #ff4d4f; /* Красный цвет */
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.3s;
}

.btn-delete:hover:not(:disabled) {
  background: #cf1322;
}

.btn-delete:disabled {
  background: #ffa39e;
  cursor: not-allowed;
  opacity: 0.6;
}
</style>