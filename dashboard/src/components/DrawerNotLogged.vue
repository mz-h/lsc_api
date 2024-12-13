<template>
  <div class="drawer drawer-end lg:hidden">
    <input id="my-drawer-4" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content">
      <!-- Page content here -->
      <label for="my-drawer-4" aria-label="Open menu" class="drawer-button">
        <img class="block" :src="Drawer" alt="Menu" />
      </label>
    </div>
    <aside class="drawer-side">
      <label
        for="my-drawer-4"
        aria-label="Close sidebar"
        class="drawer-overlay"
        ref="closeModalClick"
      ></label>
      <nav
        class="menu bg-white min-h-full w-80 p-4 text-xl justify-between text-black"
        dir="rtl"
      >
        <!-- Close button -->
        <div class="flex justify-end closeSidebar">
          <label
            for="my-drawer-4"
            class="text-gray-600 hover:text-gray-900 cursor-pointer"
          >
            <img src="../assets/images/icons/drawer.svg" alt="" />
          </label>
        </div>
        <div class="flex justify-center mt-10">
          <img src="../assets/images/icons/logo.png" alt="" />
        </div>
        <!-- First list -->
        <ul class="menu-list">
          <li>
            <RouterLink
              to="/"
              class="w-full hover:bg-primary rounded-lg flex flex-row-reverse justify-between"
            >
              <img src="../assets/images/icons/services.svg" alt="" />
              تسجيل الدخول
            </RouterLink>
          </li>
          <li>
            <a
              href="/landing"
              class="w-full hover:bg-primary rounded-lg flex flex-row-reverse justify-between"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 512 512"
                width="24"
                height="24"
              >
                <path
                  d="M164.9 24.6c-7.7-18.6-28-28.5-47.4-23.2l-88 24C12.1 30.2 0 46 0 64C0 311.4 200.6 512 448 512c18 0 33.8-12.1 38.6-29.5l24-88c5.3-19.4-4.6-39.7-23.2-47.4l-96-40c-16.3-6.8-35.2-2.1-46.3 11.6L304.7 368C234.3 334.7 177.3 277.7 144 207.3L193.3 167c13.7-11.2 18.4-30 11.6-46.3l-40-96z"
                />
              </svg>
              <span>الرئيسية</span>
            </a>
          </li>
        </ul>
      </nav>
    </aside>
  </div>
</template>

<script setup>
import Drawer from "../assets/images/icons/drawer.svg";
import { useRouter, RouterLink } from "vue-router";
import axios from "axios";
import showToastMessage from "../router/toastmessage";
import { ref } from "vue";

// Toast Message
const toastMessage = ref(null);
const showToast = ref(false);
const navigate = useRouter();
const loading = ref(false);
const closeModalClick = ref(null);

async function handleLogOut() {
  loading.value = true;
  closeModalClick.value.click();
  try {
    await axios.get("/api/method/logout", {
      withCredentials: true,
    });
    loading.value = false;
    showToastMessage("جاري تسجيل الخروج...", toastMessage, showToast);
    setTimeout(() => {
      navigate.replace("/");
    }, 1500);
  } catch (error) {
    loading.value = false;
    showToastMessage("رجاء حاول مرة اخرى لاحقاً.", toastMessage, showToast);
  }
}
</script>

<style scoped>
li,
li:hover {
  transition: all 0.3s ease-in-out;
}
.closeSidebar {
  position: absolute;
  left: 25px;
}
.toast {
  direction: rtl;
}
</style>
