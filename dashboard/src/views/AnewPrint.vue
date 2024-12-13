<template>
  <iframe :src="invoice" class="w-[21cm] h-[27cm]" frameborder="0"></iframe>
</template>

<script setup>
import { onMounted } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const invoice = route.query.invoice || "";

onMounted(() => {
  const iframe = document.querySelector("iframe");
  iframe.onload = () => {
    setTimeout(() => {
      window.close();
    }, 2000);
  };
});
</script>
