import {defineStore} from 'pinia';
import axios from 'axios';

export const useDataStore = defineStore('data', {
    state: () => ({
        tests: [],
        belbin: [],
    }),
    actions: {
        async fetchTests() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/get-all-test'); //там получаю название и url
                this.tests = response.data;
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },
        async fetchBelbin(){
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/belbin-test'); // получаю вопросы теста
                this.belbin = response.data;
                console.log('Данные загрузил', this.belbin)
                console.log(response.data)
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        }
    },
    getters: {
        getTests: (state) => state.tests,
        getBelbin: (state) => state.belbin
    },
});