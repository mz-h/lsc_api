<template>
  <LoggedInTopNav title="التسجيل" />
  <div
    class="flex items-center justify-center min-h-screen px-6 sm:px-20 py-40 bg-gray-100"
  >
    <div class="w-full max-w-lg p-6 bg-white rounded-lg shadow-md">
      <div class="img max-w-20 mx-auto">
        <img :src="Logo" alt="LSC Logo" class="block w-full" />
      </div>
      <h2 class="mb-4 text-2xl font-bold text-center text-gray-700">
        إنشاء حساب
      </h2>
      <form @submit.prevent="handleSubmit" class="text-right w-full h-auto">
        <!-- Branch select -->
        <div v-if="!form.branch" class="mb-4">
          <label
            for="firstname"
            class="block mb-2 text-sm font-medium text-gray-600"
          >
            حدد مدينة الاستفادة من الخدمات
          </label>
          <select
            v-model="form.branch"
            class="h-full w-full rounded-md border-2 bg-transparent py-0 pl-2 pr-7 text-gray-500 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm"
            style="direction: ltr"
          >
            <option v-for="branch in branchs" :key="branch" :value="branch">
              {{ branch }}
            </option>
          </select>
        </div>

        <!-- mobile_no Input -->
        <div v-if="form.branch && !sendCodeCheck" class="mb-4">
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
          <div v-if="form.branch">
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
        <div v-if="form.branch && sendCodeCheck && !correctCode" class="mb-4">
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

        <div v-if="form.branch && sendCodeCheck && correctCode">
          <!-- Full Name Input -->
          <div class="mb-4">
            <label
              for="firstname"
              class="block mb-2 text-sm font-medium text-gray-600"
            >
              اسمك الأول
            </label>
            <input
              type="text"
              id="firstname"
              v-model="form.first_name"
              class="input input-sm input-bordered w-full text-black"
              placeholder="الاسم الاول"
            />
            <p v-if="errors.first_name" class="text-red-500 text-xs mt-2">
              {{ errors.first_name }}
            </p>
          </div>

          <!-- Username Input -->
          <div class="mb-4">
            <label
              for="username"
              class="block mb-2 text-sm font-medium text-gray-600"
            >
              اسم المستخدم
            </label>
            <input
              type="text"
              id="username"
              v-model="form.username"
              class="input input-sm input-bordered w-full text-black"
              placeholder="اسم المستخدم"
            />
            <p v-if="errors.username" class="text-red-500 text-xs mt-2">
              {{ errors.username }}
            </p>
          </div>

          <!-- Password Input -->
          <div class="mb-4">
            <label
              for="password"
              class="block mb-2 text-sm font-medium text-gray-600"
            >
              كلمة المرور
            </label>
            <input
              type="password"
              id="password"
              v-model="form.password"
              class="input input-sm input-bordered w-full text-black"
              placeholder="كلمة المرور"
            />
            <p v-if="errors.password" class="text-red-500 text-xs mt-2">
              {{ errors.password }}
            </p>
          </div>

          <!-- rePassword Input -->
          <div class="mb-4">
            <label
              for="repassword"
              class="block mb-2 text-sm font-medium text-gray-600"
            >
              تأكيد كلمة المرور
            </label>
            <input
              type="password"
              id="repassword"
              v-model="repassword"
              class="input input-sm input-bordered w-full text-black"
              placeholder="تأكيد كلمة المرور"
            />
            <p v-if="errors.repassword" class="text-red-500 text-xs mt-2">
              {{ errors.repassword }}
            </p>
          </div>

          <!-- Email Input -->
          <div class="mb-4">
            <label
              for="email"
              class="block mb-2 text-sm font-medium text-gray-600"
            >
              البريد الإلكتروني
            </label>
            <input
              type="email"
              id="email"
              v-model="form.email"
              class="input input-sm input-bordered w-full text-black"
              placeholder="أدخل بريدك الإلكتروني"
            />
            <p v-if="errors.email" class="text-red-500 text-xs mt-2">
              {{ errors.email }}
            </p>
          </div>

          <!-- National ID Input -->
          <div class="mb-4">
            <label
              for="national_id"
              class="block mb-2 text-sm font-medium text-gray-600"
            >
              رقم الهوية
            </label>
            <input
              type="text"
              id="national_id"
              v-model="form.national_id"
              class="input input-sm input-bordered w-full text-black"
              placeholder="أدخل رقم الهوية"
            />
            <p v-if="errors.national_id" class="text-red-500 text-xs mt-2">
              {{ errors.national_id }}
            </p>
          </div>
        </div>

        <!-- General Error -->
        <p v-if="errors.general" class="text-red-500 text-center text-xs mt-2">
          {{ errors.general }}
        </p>

        <!-- Signup Button -->
        <div v-if="form.branch && sendCodeCheck && correctCode">
          <button type="submit" class="btn btn-primary text-white w-full">
            إنشاء حساب
          </button>
        </div>
      </form>

      <!-- Additional Links -->
      <div class="mt-6 text-center flex flex-col justify-center gap-2">
        <a
          v-if="!form.branch"
          href="https://lsc.psc-s.com/"
          class="text-sm text-blue-600 hover:underline"
        >
          لم تجد مدينتك؟ سجل ليصلك تحديثات الفروع.
        </a>

        <RouterLink to="/" class="text-sm text-blue-600 hover:underline">
          تسجيل الدخول؟
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
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import Logo from "../assets/images/icons/logo.png";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import showToastMessage from "../router/toastmessage";

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
      throw new Error("You are Not Logged In");
    }
    return response.json();
  })
  .then(() => navigate.replace("/home"))
  .catch((error) => {});

onMounted(() => {
  getBranchs();
});
// Toast Message
const toastMessage = ref(null);
const showToast = ref(false);
const loading = ref(false);
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

const branchs = ref([]);
async function getBranchs() {
  try {
    const response = await fetch(
      "/api/method/lsc_api.lsc_api.get_linked_data.get_branches"
    );
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    branchs.value = data.message.branches;
  } catch (error) {
    console.error("Error fetching user data:", error);
  }
}
// Form fields
const form = ref({
  branch: "",
  username: "",
  first_name: "",
  password: "",
  email: "",
  mobile_no: "",
  national_id: "",
});

// Error state for form fields
const errors = ref({
  username: "",
  first_name: "",
  password: "",
  repassword: "",
  email: "",
  mobile_no: "",
  national_id: "",
  general: "",
});

const router = useRouter();

// Utility function to validate form inputs
const validateForm = () => {
  let isValid = true;

  // Clear previous errors
  Object.keys(errors.value).forEach((key) => {
    errors.value[key] = "";
  });

  // All fields are required
  for (const [key, value] of Object.entries(form.value)) {
    if (!value.trim()) {
      errors.value[key] = `هذا الحقل مطلوب.`;
      isValid = false;
    }
  }

  // Password validation
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
  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(form.value.email)) {
    errors.value.email = "برجاء ادخال إيميل صحيح.";
    isValid = false;
  }

  // mobile_no validation for Egyptian and Saudi Arabia numbers
  const saudimobile_noRegex = /^9665\d{8}$/;
  if (!saudimobile_noRegex.test(form.value.mobile_no)) {
    errors.value.mobile_no = "برجاء إدخال رقم هاتف سعودي.";
    isValid = false;
  }

  // National ID validation (assuming it follows a similar pattern as the mobile_no)
  const saudiNationalIdRegex = /^(1|2)\d{9}$/;
  if (!saudiNationalIdRegex.test(form.value.national_id)) {
    errors.value.national_id = "برجاء إدخال رقم هوية سعودية.";
    isValid = false;
  }

  return isValid;
};

// Handle registration form submission
const handleSubmit = async () => {
  if (!validateForm()) {
    return;
  }
  loading.value = true;

  try {
    const response = await axios.post(
      "/api/method/lsc_api.lsc_api.register.register",
      { data: form.value },
      {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      }
    );
    loading.value = false;
    if (response.data.message.status === "success") {
      showToastMessage("تم التسجيل بنجاح!", toastMessage, showToast);
      setTimeout(() => {
        router.replace("/");
      }, 1500);
    } else {
      errors.value.general = "Registration failed. Please try again.";
    }
  } catch (error) {
    loading.value = false;
    if (error.response) {
      // Handle specific error from the server
      if (error.response.data.message.message.includes("username")) {
        showToastMessage(
          "الاسم مستخدم مسبقاً، من فضلك اختار اسم مختلف.",
          toastMessage,
          showToast
        );
        errors.value.username =
          "Username already exists. Please choose another.";
      } else if (error.response.data.message.message.includes("mobile_no")) {
        showToastMessage(
          "الرقم مستخدم مسبقاً، من فضلك اختار رقم مختلف.",
          toastMessage,
          showToast
        );
        errors.value.mobile_no = "mobile_no Already Exist";
      } else if (error.response.data.message.message.includes("email")) {
        errors.value.email = "Email Already Exist";
        showToastMessage(
          "الايميل مستخدم مسبقاً، من فضلك اختار ايميل مختلف.",
          toastMessage,
          showToast
        );
      } else {
        errors.value.general =
          error.response.data.message ||
          "An error occurred during registration. Please try again.";
      }
    } else {
      // Handle network or other errors
      showToastMessage(
        "خطأ في الشبكة، تأكد من اتصالك بالإنترنت",
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
</style>
