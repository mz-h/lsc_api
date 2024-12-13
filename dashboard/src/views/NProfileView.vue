<template>
  <LoggedInTopNav title="معلومات شخصية" :backArrow="false" />
  <div
    class="prof flex flex-col w-full px-6 gap-8 mt-24 lg:mt-40 pb-24 max-w-96 mx-auto"
  >
    <RouterLink :to="{ name: 'UserSettingsView' }">
      <div class="brief flex gap-4">
        <img
          v-if="userData.user_image"
          :src="userData.user_image"
          alt="ProfilePic"
          class="w-1/2 max-w-24 block rounded-lg"
        />
        <img
          v-else
          :src="ProfilePic"
          alt="ProfilePic"
          class="w-1/2 max-w-24 block"
        />
        <div class="brief-info text-xs flex flex-col justify-evenly">
          <h2 class="text-black font-bold">{{ userData.full_name }}</h2>
          <p class="font-medium">
            رقم الهوية:
            <span>{{ userData.custom_id_number }}</span>
          </p>
        </div>
      </div>
    </RouterLink>
    <RouterLink :to="{ name: 'PersonalinfoView' }">
      <div class="personalInfo flex justify-between items-center">
        <div class="rig flex gap-2">
          <img :src="Profile" alt="ProfileIcon" />
          <p class="text-black">معلومات شخصية</p>
        </div>
        <img :src="LeftArrowBlack" alt="Icon" />
      </div>
    </RouterLink>
    <RouterLink :to="{ name: 'ResidentialinfoView' }">
      <div class="accomInfo flex justify-between items-center">
        <div class="rig flex gap-2">
          <img :src="HomeHash" alt="HomeIcon" />
          <p class="text-black">معلومات الإقامة</p>
        </div>
        <img :src="LeftArrowBlack" alt="Icon" />
      </div>
    </RouterLink>
    <RouterLink :to="{ name: 'PowerofAttView' }">
      <div class="accomInfo flex justify-between items-center">
        <div class="rig flex gap-2 items-center text-black">
          <font-awesome-icon icon="fa-regular fa-file" class="w-6 h-6" />
          <p class="text-black">إرفاق توكيل</p>
        </div>
        <img :src="LeftArrowBlack" alt="Icon" />
      </div>
    </RouterLink>
    <RouterLink :to="{ name: 'AllInvoicesView' }">
      <div class="accomInfo flex justify-between items-center">
        <div class="rig flex gap-2 items-center text-black">
          <font-awesome-icon icon="fa-regular fa-credit-card" class="w-6 h-6" />
          <p class="text-black">الفواتير السابقة</p>
        </div>
        <img :src="LeftArrowBlack" alt="Icon" />
      </div>
    </RouterLink>
    <div class="terms flex justify-between">
      <RouterLink :to="{ name: 'TermsView' }">
        <div class="accomInfo flex justify-between items-center">
          <div class="rig flex gap-2 items-center text-primary">
            <p class="text-primary">شروط الاستخدام</p>
          </div>
        </div>
      </RouterLink>
      <RouterLink :to="{ name: 'PrivacyPolicy' }">
        <div class="accomInfo flex justify-between items-center">
          <div class="rig flex gap-2 items-center text-primary">
            <p class="text-primary">سياسة الخصوصية</p>
          </div>
        </div>
      </RouterLink>
    </div>
    <div class="accomInfo flex justify-between items-center">
      <label class="label cursor-pointer w-full">
        <span class="label-text">اللغة</span>
        <div class="flex gap-2">
          <span class="label-text">عربي</span>
          <input
            type="checkbox"
            class="toggle bg-white"
            :checked="isArabic"
            @change="toggleLanguage"
          />
          <span class="label-text">English</span>
        </div>
      </label>
    </div>
  </div>
  <Loader v-if="loading" />
  <BottomNav />
</template>

<script setup>
import BottomNav from "@/components/BottomNav.vue";
import { RouterLink } from "vue-router";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import Profile from "../assets/images/icons/profile.svg";
import LeftArrowBlack from "../assets/images/icons/LeftArrowBlack.svg";
import HomeHash from "../assets/images/icons/home-hashtag.svg";
import ProfilePic from "../assets/images/profile.png";
import { useRouter } from "vue-router";
import { onMounted, ref } from "vue";
import Loader from "@/components/Loader.vue";
const loading = ref(false);

const navigate = useRouter();
const requestOptions = {
  method: "GET",
  headers: { Cookie: document.cookie },
  redirect: "follow",
};

fetch("/api/method/frappe.auth.get_logged_user", requestOptions)
  .then((response) => {
    if (!response.ok) {
      throw new Error("You are not logged In");
    }
    return response.json();
  })
  .then()
  .catch(() => navigate.replace("/"));

const userData = ref({
  full_name: "",
  custom_id_number: null,
  user_image: null,
  language: "",
});

const isArabic = ref(true);
const toggleLanguage = async () => {
  // Call your API to switch language
  const selectedLang = isArabic.value ? "en" : "ar"; // Toggle between Arabic and English
  const formData = new FormData();
  formData.append("language", selectedLang);
  try {
    loading.value = true;
    const response = await fetch(
      "/api/method/lsc_api.lsc_api.update_user_data.update_user_data",
      {
        method: "PATCH",
        body: formData, // Send the formData
      }
    );
    setTimeout(() => {
      loading.value = false;
      window.location.reload();
    }, 1000);
  } catch (error) {
    console.error("Error changing language:", error);
  }

  // Toggle language state
  isArabic.value = !isArabic.value;
};

const getUserData = async () => {
  try {
    const response = await fetch(
      "/api/method/lsc_api.lsc_api.get_user_data.get_user_data"
    );
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    userData.value = data.message.user_data;
    if (userData.value.language == "en") {
      isArabic.value = false;
    }
  } catch (error) {
    console.error("Error fetching user data:", error);
  }
};

onMounted(() => {
  getUserData();
});
</script>
