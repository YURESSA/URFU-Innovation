<template>
    <chapter-one-header></chapter-one-header>
  </div>
</template>

<script setup>
import { useDataStore } from '@/stores/store.js';
import {computed} from 'vue';
import ChapterOneHeader from '@/components/belbin/chapter-one-header.vue';

const store = useDataStore();

const questions = computed(() => store.getBelbin);
</script>

<style scoped>

</style>