<template>
  <div
    class="navbar shadow-sm place-self-center bg-white z-10 text-black fixed top-0"
  >
    <div class="navbar lg:w-4/5 mx-auto flex justify-between">
      <div class="navbar-start w-auto">
        <RouterLink to="/notifications" v-if="showMenu">
          <font-awesome-icon
            icon="fa-regular fa-bell"
            :class="{ 'text-red-500': notificationsState.hasNewNotifications }"
          />
        </RouterLink>
      </div>

      <div class="navbar-center w-auto">
        <h1 class="font-black">{{ title }}</h1>
      </div>
      <div class="navbar-end w-auto">
        <RouterLink v-if="backArrow" @click.prevent="goBack" to="#">
          <img :src="arrowBackWhite" alt="Icon" />
        </RouterLink>
        <template v-else>
          <Drawer v-if="showMenu" />
          <DrawerNotLogged v-else />
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.text-red-500 {
  color: #ef4444; /* Tailwind CSS red color */
}
.navbar {
  direction: ltr;
}
</style>

<script setup>
import arrowBackWhite from "../assets/images/icons/arrow_back_black.svg";
import { useRouter } from "vue-router";
import Drawer from "./Drawer.vue";
import { ref } from "vue";
import DrawerNotLogged from "./DrawerNotLogged.vue";
import { notificationsState } from "../router/notificationsState";

const navigate = useRouter();
const showMenu = ref(true);

const requestOptions = {
  method: "GET",
  headers: { Cookie: document.cookie },
  redirect: "follow",
};
fetch(
  "/api/method/frappe.auth.get_logged_user",
  requestOptions
)
  .then((response) => {
    if (!response.ok) {
      throw new Error("You are not logged In");
    }
    return response.json();
  })
  .then((data) => {})
  .catch(() => {
    showMenu.value = false;
  });

const router = useRouter();
const goBack = () => {
  router.go(-1); // Navigate to the previous route in history
};

defineProps({
  title: String,
  backArrow: Boolean,
});

</script>
