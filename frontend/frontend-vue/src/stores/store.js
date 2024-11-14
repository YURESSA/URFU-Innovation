import { defineStore } from 'pinia';
import axios from 'axios';

export const useDataStore = defineStore('data', {
  state: () => ({
    tests: [],
  }),
  actions: {
    async fetchTests() {
      try {
        const response = await axios.get('https://29.javascript.htmlacademy.pro/kekstagram/data'); //там получаю название и url 
        this.tests = response.data;
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    },
  },
  getters: {
    getTests: (state) => state.tests,
  },
});