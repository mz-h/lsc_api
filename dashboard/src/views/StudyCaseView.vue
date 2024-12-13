<template>
  <LoggedInTopNav :title="servName" :backArrow="true" />
  <div class="w-full h-screen flex items-center justify-center p-8 bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <label class="form-control w-full">
          <input
            v-model="title"
            type="text"
            placeholder="الاسم"
            class="input input-bordered w-full"
          />
          <p v-if="errors.title" class="text-red-600 text-sm">
            {{ errors.title }}
          </p>
        </label>

        <label class="form-control w-full">
          <textarea
            v-model="case_description"
            class="textarea textarea-bordered bg-white h-24 w-full"
            placeholder="التفاصيل"
          ></textarea>
          <p v-if="errors.case_description" class="text-red-600 text-sm">
            {{ errors.case_description }}
          </p>
        </label>

        <label class="form-control w-full">
          <div class="label">
            <span class="label-text-alt">إرفاق ملف</span>
          </div>
          <input
            ref="file"
            type="file"
            class="file-input file-input-bordered file-input-sm w-full max-w-xs"
          />
        </label>

        <button type="submit" class="btn btn-primary w-full">إرسال</button>
      </form>

      <div
        v-if="message"
        class="mt-4 p-4 bg-green-100 text-green-800 border border-green-300 rounded"
        :class="messageClass"
      >
        {{ message }}
      </div>
    </div>
  </div>
  <Loader v-if="loading" />
  <BottomNav />
</template>

<script setup>
import { ref } from "vue";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import BottomNav from "@/components/BottomNav.vue";
import Loader from "@/components/Loader.vue";
import axios from "axios";
import { useRoute } from "vue-router";

const loading = ref(false);
const case_description = ref("");
const title = ref("");
const file = ref(null);
const message = ref("");
const messageClass = ref("");
const errors = ref({});
const route = useRoute();
const servName = route.query.elemnt || "";

// Validate form input
const validateForm = () => {
  errors.value = {};
  if (!title.value || title.value.length < 5) {
    errors.value.title = "الاسم مطلوب ويجب أن يكون 5 أحرف على الأقل.";
  }
  if (!case_description.value || case_description.value.length < 5) {
    errors.value.case_description =
      "التفاصيل مطلوبة ويجب أن تكون 5 أحرف على الأقل.";
  }
  return Object.keys(errors.value).length === 0;
};

const handleSubmit = () => {
  if (!validateForm()) {
    return;
  }

  loading.value = true;
  const formData = new FormData();
  formData.append("name", servName);
  formData.append("title", title.value);
  formData.append("description", case_description.value);
  if (file.value && file.value.files.length > 0) {
    formData.append("file", file.value.files[0]);
  }

  axios
    .post(
      "/api/method/lsc_api.lsc_api.create_case_study.create_case_study",
      formData
    )
    .then((response) => {
      loading.value = false;
      const data = response.data;
      console.log(data);
      if (data.message.status === "success") {
        message.value = "تم الحجز بنجاح";
        messageClass.value =
          "bg-green-100 text-green-800 border border-green-300";
      } else {
        message.value = "حدث خطأ اثناء الحجز";
        messageClass.value = "bg-red-100 text-red-800 border border-red-300";
      }
    })
    .catch((error) => {
      loading.value = false;
      messageClass.value = "bg-red-100 text-red-800 border border-red-300";
      if (error.response.data.exception.includes("hours quota")) {
        message.value = "رصيد الساعات المتبقية غير كافي.";
      } else if (error.response.data.exception.includes("expire_date")) {
        message.value = "التوكيل المرفق غير صالح، برجاء مراجعة تاريخ التوكيل.";
      } else {
        message.value = "حدث خطأ اثناء حجز الخدمة";
      }
    });
};
</script>

<style scoped>
input {
  background-color: white;
}
.text-red-600 {
  color: #dc2626;
}
</style>
