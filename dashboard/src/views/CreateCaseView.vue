<template>
  <LoggedInTopNav :title="servName" :backArrow="true" />

  <div class="w-full h-screen flex items-center justify-center p-8 bg-gray-100">
    <div class="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <label class="form-control w-full">
          <select
            class="select select-bordered w-full bg-white px-8"
            v-model="selectedType"
          >
            <option v-for="type in caseTypes" :key="type" :value="type">
              {{ type }}
            </option>
          </select>
        </label>

        <label class="form-control w-full">
          <input
            v-model="title"
            type="text"
            placeholder="القضية"
            class="input input-bordered w-full"
          />
        </label>


        <label
        for="dropzone-file"
        class="flex flex-col items-center justify-center h-full w-full h-16 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600 bg-white"
      >
        <div class="flex flex-col items-center justify-center pt-2 pb-2">
          <font-awesome-icon
            v-if="!changeIcon"
            icon="fa-solid fa-cloud-arrow-up"
          />
          <font-awesome-icon v-else icon="fa-solid fa-circle-check" />
          <span class="font-semibold">
            {{ changeIcon ? "تم إرفاق الملف" : "اضغط هنا للإرفاق" }}
          </span>
          <p class="text-xs text-gray-500 dark:text-gray-400 truncate">
            {{ changeIcon ? upFile : " صور أو ملفات أو وسائط" }}
          </p>
        </div>
        <input
          @change="handleFileChange"
          ref="file"
          id="dropzone-file"
          type="file"
          class="hidden"
        />
      </label>

        <!-- <label class="form-control w-full">
          <div class="label">
            <span class="label-text-alt">إرفاق ملف</span>
          </div>
          <input
            ref="file"
            type="file"
            class="file-input file-input-bordered file-input-sm w-full max-w-xs"
          />
        </label> -->

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
const title = ref("");
const file = ref(null);
const upFile = ref(null);
const changeIcon = ref(false);
const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    changeIcon.value = true; // Change icon once file is selected
    upFile.value = file.name;
  }
};
const message = ref("");
const messageClass = ref("");
const route = useRoute();
const servName = route.query.elemnt || "";
const caseTypes = ref([
  "قضية جنائية",
  "قضية عمالية",
  "قضية احوال شخصية",
  "قضية عامة",
]);
const selectedType = ref("");

const handleSubmit = () => {
  // Validation: Check if the title is empty or less than 5 characters
  if (title.value.length < 5) {
    message.value = "الرجاء إدخال عنوان القضية (على الأقل 5 أحرف)";
    messageClass.value = "bg-red-100 text-red-800 border border-red-300";
    return; // Stop the form submission if validation fails
  }

  // Validation: Check if the case type is selected
  if (!selectedType.value) {
    message.value = "الرجاء اختيار نوع القضية";
    messageClass.value = "bg-red-100 text-red-800 border border-red-300";
    return; // Stop the form submission if validation fails
  }

  loading.value = true;
  const formData = new FormData();
  formData.append("name", servName);
  formData.append("title", title.value);
  formData.append("department", selectedType.value);
  if (file.value && file.value.files.length > 0) {
    formData.append("file", file.value.files[0]);
  }

  axios
    .post("/api/method/lsc_api.lsc_api.create_case.create_case", formData)
    .then((response) => {
      loading.value = false;
      const data = response.data;
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
</style>
