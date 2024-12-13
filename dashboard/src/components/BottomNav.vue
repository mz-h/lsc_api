<template>
  <div class="btm-nav bg-white lg:hidden">
    <router-link
      v-for="(navLink, index) in nav"
      :key="index"
      :to="`/${navLink.dir}`"
    >
      <img :src="navLink.img" :alt="navLink.title" />
      <span>{{ navLink.title }}</span>
    </router-link>
  </div>
</template>

<script setup>
import profileIcon from "../assets/images/icons/profile.svg";
import homeIcon from "../assets/images/icons/home.svg";
import requestsIcon from "../assets/images/icons/requests.svg";
import servicesIcon from "../assets/images/icons/services.svg";
import { ref } from "vue";
import { RouterLink } from "vue-router";

const nav = ref([
  { dir: "home", img: homeIcon, title: "الرئيسية" },
  { dir: "services", img: servicesIcon, title: "الخدمات" },
  { dir: "requests", img: requestsIcon, title: "الطلبات" },
  { dir: "profile", img: profileIcon, title: "حسابك" },
]);
</script>

<style scoped>
span {
  @apply text-black text-sm px-2  p-1 text-nowrap rounded-lg duration-300 cursor-pointer;
}

.router-link-active span {
  @apply bg-primaryLight bg-opacity-50 text-primary font-bold;
}
.btm-nav {
  box-shadow: 0 -4px 20px 1px rgb(0 0 0 / 10%);
}
</style>
