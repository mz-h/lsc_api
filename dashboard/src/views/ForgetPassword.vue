<template>
  <LoggedInTopNav title="إستعادة كلمة المرور" />
  <div
    class="flex px-6 sm:px-20 items-center justify-center min-h-screenpx-6 py-40 bg-gray-100 rtl"
  >
    <div class="w-full max-w-sm p-6 bg-white rounded-lg shadow-md">
      <div class="img max-w-20 mx-auto">
        <img :src="Logo" alt="LSC Logo" class="block w-full" />
      </div>
      <h2 class="mb-4 text-2xl font-bold text-center text-gray-700">
        إستعادة كلمة المرور
      </h2>
      <form @submit.prevent="handleReset" class="text-right">
        <!-- mobile_no Input -->
        <div v-if="!sendCodeCheck" class="mb-4">
          <label
            for="mobile_no"
            class="block mb-2 text-sm font-medium text-gray-600"
          >
            رقم الهاتف
            <!-- 966 5458921 -->
          </label>
          <div class="relative mt-2 rounded-md shadow-sm w-full">
            <input
              type="tel"
              id="mobile_no"
              v-model="form.mobile_no"
              class="input input-sm input-bordered w-full text-black"
              placeholder="9665XXXXXXXX"
            />
          </div>
          <p v-if="errors.mobile_no" class="text-red-500 text-xs mt-2">
            {{ errors.mobile_no }}
          </p>
          <div>
            <button
              @click="() => sendCode(form.mobile_no)"
              type="button"
              class="btn btn-primary text-white w-full mt-4"
            >
              إرسال رمز تأكيد
            </button>
          </div>
        </div>

        <!-- Code Checker Input -->
        <div v-if="sendCodeCheck && !correctCode" class="mb-4">
          <label
            for="optCheck"
            class="block mb-2 text-sm font-medium text-gray-600"
          >
            رمز التحقق
            <!-- XXXXXX -->
          </label>
          <div class="relative mt-2 rounded-md shadow-sm w-full">
            <input
              type="tel"
              id="optCheck"
              v-model="otp"
              class="input input-sm input-bordered w-full text-black"
              placeholder="XXXXXX"
            />
          </div>
          <div>
            <button
              @click="() => checkOtp(form.mobile_no, String(otp))"
              type="button"
              class="btn btn-primary text-white w-full mt-4"
            >
              تحقق من الرمز
            </button>
          </div>
        </div>

        <div v-if="sendCodeCheck && correctCode">
          <!-- Password Input -->
          <div class="mb-4">
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
          <div class="mb-6">
            <label
              for="repassword"
              class="block mb-2 text-sm font-medium text-gray-600"
              >كلمة المرور</label
            >
            <input
              type="password"
              id="repassword"
              v-model="repassword"
              class="input input-bordered w-full text-black"
              placeholder="أدخل كلمة المرور"
              autocomplete="current-password"
            />
            <!-- Error Message for Password -->
            <p v-if="errors.repassword" class="text-red-500 text-xs mt-2">
              {{ errors.repassword }}
            </p>
          </div>
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
fetch("/api/method/frappe.auth.get_logged_user", requestOptions)
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

const sendCodeCheck = ref(false);
const correctCode = ref(false);
const repassword = ref("");

async function sendCode(phone) {
  // mobile_no validation for Egyptian and Saudi Arabia numbers
  const saudimobile_noRegex = /^9665\d{8}$/;
  if (!saudimobile_noRegex.test(form.value.mobile_no)) {
    errors.value.mobile_no = "برجاء إدخال رقم هاتف سعودي.";
    sendCodeCheck.value = false;
  } else {
    loading.value = true;
    const response = await axios.post(
      "/api/method/lsc_api.lsc_api.sms_api.sms_api",
      { phone_number: phone },
      {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      }
    );
    loading.value = false;
    if (response.data.message.status == "success") {
      sendCodeCheck.value = true;
    } else {
      showToastMessage(
        ".برجاء التأكد من الرقم وإعادة المحاولة",
        toastMessage,
        showToast
      );
    }
  }
  loading.value = false;
}
const otp = ref("");
async function checkOtp(phone, num) {
  if (num.length != 6) {
    showToastMessage("برجاء إدخال 6 أرقام.", toastMessage, showToast);
    return;
  }
  loading.value = true;
  const response = await axios.post(
    "/api/method/lsc_api.lsc_api.sms_api.validateOTP",
    { data: { otp: num, phone_number: phone } },
    {
      headers: {
        "Content-Type": "application/json",
      },
      withCredentials: true,
    }
  );
  loading.value = false;
  if (response.data.message.status == "success") {
    correctCode.value = true;
  } else {
    showToastMessage(
      "الكود غير صحيح، الرجاء المحاولة مرةأخرى.",
      toastMessage,
      showToast
    );
  }
  loading.value = false;
}

// Form Data
const form = ref({
  password: "",
  mobile_no: "",
});

// Error state for form fields
const errors = ref({
  password: "",
  repassword: "",
  mobile_no: "",
  general: "",
});

// Form Validation Function
const validateForm = () => {
  const passwordRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  if (!passwordRegex.test(form.value.password)) {
    errors.value.password =
      "كلمة المرور يجب ان لا تقل عن 8 أحرف، ويجب أن تحتوي على أحرف كبيرة وصغيرة وأرقام ورموز.";
    isValid = false;
  }

  if (form.value.password !== repassword.value) {
    errors.value.repassword = "كلمات المرور غير متطابقة.";
    isValid = false;
  }
  return !errors.password && !errors.repassword;
};

// Handle Login
const handleReset = async () => {
  if (!validateForm()) return;
  loading.value = true;

  const formData = new FormData();
  formData.append("mobile_no", form.mobile_no);
  formData.append("new_password", form.password);

  const response = await fetch(
    "/api/method/lsc_api.lsc_api.update_user_data.update_user_data",
    {
      method: "PATCH",
      body: formData, // Send the formData
    }
  );
  const data = await response.json();
  console.log(data)
  loading.value = false;
  if (response.data.message.status === "success") {
    showToastMessage("تم التسجيل بنجاح!", toastMessage, showToast);
    setTimeout(() => {
      router.replace("/");
    }, 1500);
  } else {
    errors.value.general = "Failed. Please try again.";
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
