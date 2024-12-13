<template>
  <LoggedInTopNav title="تسجيل الدخول" />
  <div
    class="flex px-6 sm:px-20 items-center justify-center min-h-screenpx-6 py-40 bg-gray-100 rtl"
  >
    <div class="w-full max-w-sm p-6 bg-white rounded-lg shadow-md">
      <div class="img max-w-20 mx-auto">
        <img :src="Logo" alt="LSC Logo" class="block w-full" />
      </div>
      <h2 class="mb-4 text-2xl font-bold text-center text-gray-700">
        تسجيل الدخول
      </h2>
      <form @submit.prevent="handleLogin" class="text-right">
        <!-- Username/Email Input -->
        <div class="mb-4">
          <label
            for="username"
            class="block mb-2 text-sm font-medium text-gray-600"
            >اسم المستخدم</label
          >
          <input
            type="text"
            id="username"
            v-model="form.username"
            class="input input-bordered w-full text-black"
            placeholder="اسم المستخدم"
            autocomplete="name"
          />
          <!-- Error Message for Username -->
          <p v-if="errors.username" class="text-red-500 text-xs mt-2">
            {{ errors.username }}
          </p>
        </div>

        <!-- Password Input -->
        <div class="mb-6">
          <label
            for="password"
            class="block mb-2 text-sm font-medium text-gray-600"
            >كلمة المرور</label
          >
          <input
            type="password"
            id="password"
            v-model="form.password"
            class="input input-bordered w-full text-black"
            placeholder="أدخل كلمة المرور"
            autocomplete="current-password"
          />
          <!-- Error Message for Password -->
          <p v-if="errors.password" class="text-red-500 text-xs mt-2">
            {{ errors.password }}
          </p>
        </div>

        <!-- General Error Message -->
        <p v-if="errors.general" class="text-red-500 text-center text-xs mt-2">
          {{ errors.general }}
        </p>

        <!-- Login Button -->
        <div>
          <button type="submit" class="btn btn-primary w-full text-white">
            تسجيل الدخول
          </button>
        </div>
      </form>

      <!-- Additional Links -->
      <div class="mt-6 text-center">
        <a href="#" class="text-sm text-blue-600 hover:underline">
          هل نسيت كلمة المرور؟
        </a>
      </div>
      <div class="mt-2 text-center">
        <RouterLink to="/signup" class="text-sm text-blue-600 hover:underline">
          لا تملك حساباً؟إنشاء حساب
        </RouterLink>
      </div>
    </div>
  </div>

  <!-- Toast Notification -->
  <div v-if="showToast" class="relative">
    <div class="toast bottom-20 left-1/2 -translate-x-1/2">
      <div class="alert alert-info bg-white border-2 border-primary">
        <span>{{ toastMessage }}</span>
      </div>
    </div>
  </div>
  <!-- Loading? -->
  <div
    v-if="loading"
    class="loader absolute z-20 flex bg-gray-200 bg-opacity-40 justify-center items-center w-screen h-screen left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
  >
    <span class="loading text-primary loading-ring loading-lg"></span>
  </div>
  <!-- END LOADING -->
</template>

<script setup>
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import Logo from "../assets/images/icons/logo.png";
import axios from "axios";
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import showToastMessage from "../router/toastmessage";

// Toast Message
const toastMessage = ref(null);
const showToast = ref(false);
const loading = ref(false);

const navigate = useRouter();

const requestOptions = {
  method: "GET",
  headers: { Cookie: document.cookie },
  redirect: "follow",
};
// Check loggedin
fetch(
  "/api/method/frappe.auth.get_logged_user",
  requestOptions
)
  .then((response) => {
    if (!response.ok) {
      // error 403
      throw new Error("You are Not Logged In");
    }
    // no error,
    return response.json();
  })
  .then(() => navigate.replace("/home"))
  .catch((error) => {});

// Form Data
const form = ref({
  username: "",
  password: "",
});

// Errors Object
const errors = reactive({
  username: null,
  password: null,
  general: null,
});

// Form Validation Function
const validateForm = () => {
  errors.username = form.value.username ? null : "يرجى إدخال اسم المستخدم.";
  errors.password = form.value.password ? null : "يرجى إدخال كلمة المرور.";

  return !errors.username && !errors.password;
};

// Handle Login
const handleLogin = async () => {
  if (!validateForm()) return;

  loading.value = true;

  try {
    const response = await axios.post(
      "/api/method/lsc_api.lsc_api.login.login",
      { data: form.value },
      {
        headers: {
          "Content-Type": "application/json",
          withCredentials: true,
        },
      }
    );

    if (response.data.message.status !== "fail") {
      showToastMessage("تم تسجيل الدخول بنجاح!", toastMessage, showToast);
      loading.value = false;
      navigate.replace("/home"); // Redirect to the profile page after login
    } else {
      showToastMessage(
        "خطأ: " + response.data.message,
        toastMessage,
        showToast
      ); // Display error message
      loading.value = false;
    }
  } catch (error) {
    loading.value = false;
    if (error.response && error.response.data) {
      // Handling specific API error response
      if (
        error.response.data.message.message === "Invalid email or password."
      ) {
        showToastMessage(
          "البريد الإلكتروني أو كلمة المرور غير صحيحة.",
          toastMessage,
          showToast
        );
      } else {
        showToastMessage(
          "حدث خطأ غير متوقع. حاول مرة أخرى لاحقًا.",
          toastMessage,
          showToast
        );
      }
    } else {
      // Handling generic network error
      showToastMessage(
        "فشل الاتصال بالخادم. يرجى التحقق من الاتصال بالإنترنت.",
        toastMessage,
        showToast
      );
    }
  }
};


</script>

<style scoped>
input {
  background: #f0f0f0;
}

.rtl {
  direction: rtl;
  text-align: right;
}
</style>
