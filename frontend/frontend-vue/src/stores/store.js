import {defineStore} from 'pinia';
import axios from 'axios';

export const useDataStore = defineStore('data', {
    state: () => ({
        tests: [],
        belbin: [],
        belbinResult: []
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
                console.log('Данные загрузил')
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },
        async fetchBelbinResult(){
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/get-test-results'); // получаю результаты теста Белбина
                this.belbinResult = response.data;
                console.log('Данные загрузил')
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        }
    },
    getters: {
        getTests: (state) => state.tests,
        getBelbin: (state) => state.belbin,
        getBelbinResult: (state) => state.belbinResult,
    },
});