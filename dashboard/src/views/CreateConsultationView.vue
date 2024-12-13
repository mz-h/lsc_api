<template>
  <LoggedInTopNav :title="servName" :backArrow="true" />

  <div
    class="w-full h-screen flex items-center justify-center p-8 bg-gray-100 my-8 lg:my-24"
  >
    <div class="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <label class="form-control w-full text-black"> عنوان الاستشارة </label>
        <input
          v-model="title"
          type="text"
          placeholder="يرجى ادخال عنوان الاستشارة الخاص بك"
          class="input input-bordered w-full"
        />

        <label
          v-if="servName != 'استشارة كتابية'"
          class="form-control w-full text-black"
        >
          اختيار الوقت
        </label>
        <div
          v-if="servName != 'استشارة كتابية'"
          class="flex flex-col gap-2 w-full"
        >
          <VueDatePicker
            v-model="date"
            :enable-time-picker="false"
            :min-date="minDate"
            :max-date="maxDate"
            range-separator="-"
            prevent-min-max-navigation
            class="text-right"
            placeholder="الوقت"
            text-input
          />
          <ul id="timetable" class="grid w-full grid-cols-3 gap-2">
            <li v-for="(slot, index) in availSlots" :key="index">
              <input
                type="radio"
                :id="'slot-' + index"
                :value="slot"
                v-model="selectedSlot"
                class="hidden peer"
                name="timetable"
              />
              <label
                :for="'slot-' + index"
                style="direction: ltr"
                class="inline-flex items-center justify-center w-full p-1 text-xs font-medium text-center hover:text-gray-900 dark:hover:text-white bg-white dark:bg-gray-800 border rounded-lg cursor-pointer text-gray-500 border-gray-200 dark:border-gray-700 dark:peer-checked:border-primary peer-checked:border-primary dark:hover:border-gray-600 dark:peer-checked:text-white peer-checked:bg-primary peer-checked:text-white hover:bg-gray-50 dark:text-gray-400 dark:hover:bg-gray-600 dark:peer-checked:bg-primary bg-white"
              >
                {{ formatTime(slot.fromTime) }}
              </label>
            </li>
          </ul>
        </div>
        <div
          v-if="message"
          class="mt-4 p-4 bg-green-100 text-green-800 border border-green-300 rounded"
          :class="messageClass"
        >
          {{ message }}
        </div>
        <label class="form-control w-full text-black"> شرح مختصر </label>
        <textarea
          v-model="case_description"
          class="textarea textarea-bordered bg-white h-24 w-full"
          placeholder="تفاصيل الاستشارة"
        ></textarea>

        <div class="flex items-center justify-center w-full bg-white">
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
        </div>

        <button type="submit" class="btn btn-primary w-full">إرسال</button>
      </form>
    </div>
  </div>
  <Loader v-if="loading" />
  <BottomNav />
</template>

<script setup>
import { ref, computed, watch } from "vue";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import BottomNav from "@/components/BottomNav.vue";
import Loader from "@/components/Loader.vue";
import axios from "axios";
import { useRoute } from "vue-router";
import { addDays } from "date-fns";

const minDate = computed(() => new Date());
const maxDate = computed(() => addDays(new Date(), 15));
const upFile = ref(null);
const changeIcon = ref(false);
const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    changeIcon.value = true; // Change icon once file is selected
    upFile.value = file.name;
  }
};
const date = ref(new Date());
const loading = ref(false);
const case_description = ref("");
const title = ref("");
const file = ref(null);
const message = ref("");
const messageClass = ref("");
const route = useRoute();
const servName = route.query.elemnt || "";
const availSlots = ref([]);
const selectedSlot = ref(null);
const formatTime = (time) => {
  const [hours, minutes] = time.split(":");
  const date = new Date();
  date.setHours(hours, minutes);

  // Convert to 12-hour format
  const options = { hour: "numeric", minute: "numeric", hour12: true };
  return date.toLocaleString("en-US", options);
};

const convertDate = (date) => {
  const d = new Date(date);
  const day = String(d.getDate()).padStart(2, "0"); // Get the day and pad it with 0 if needed
  const month = String(d.getMonth() + 1).padStart(2, "0"); // Get the month (getMonth is 0-indexed) and pad with 0
  const year = String(d.getFullYear()).slice(-2); // Get last 2 digits of the year
  return `${year}-${month}-${day}`;
};

const handleSubmit = () => {
  if (title.value.length < 5) {
    message.value = "الرجاء إدخال العنوان (على الأقل 5 أحرف)";
    messageClass.value = "bg-red-100 text-red-800 border border-red-300";
    return;
  }
  if (case_description.value.length < 5) {
    message.value = "الرجاء إدخال التفاصيل (على الأقل 5 أحرف)";
    messageClass.value = "bg-red-100 text-red-800 border border-red-300";
    return;
  }
  loading.value = true;
  const formData = new FormData();
  formData.append("consultation_name", servName);
  formData.append("title", title.value);
  formData.append("date", convertDate(date.value));
  if (selectedSlot.value) {
    formData.append("start_time", selectedSlot.value.fromTime);
    formData.append("end_time", selectedSlot.value.toTime);
  }
  formData.append("description", case_description.value);
  if (file.value && file.value.files.length > 0) {
    formData.append("file", file.value.files[0]);
  }

  axios
    .post(
      "/api/method/lsc_api.lsc_api.create_consultation.create_consultation",
      formData
    )
    .then((response) => {
      loading.value = false;
      const data = response.data;
      if (data.message.status === "جديد") {
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
watch(date, async (newDate) => {
  loading.value = true;
  if (newDate) {
    try {
      const response = await axios.post(
        "/api/method/lsc_api.lsc_api.doctype.employee_appointment.employee_appointment.get_availability_data",
        {
          date: newDate,
        }
      );
      loading.value = false;
      message.value = "";
      availSlots.value = response.data.message.slot_details[0].avail_slot.map(
        (slot) => {
          return {
            fromTime: slot.from_time,
            toTime: slot.to_time,
          };
        }
      );
    } catch (error) {
      loading.value = false;
      if (error.response.data.exception.includes("holiday")) {
        message.value = "هذا اليوم عطلة، برجاء اختيار يوم أخر.";
        messageClass.value = "bg-red-100 text-red-800 border border-red-300";
        availSlots.value = [];
      } else {
        message.value = "حدث خطأ اثناء اختيار اليوم، الرجاء المحاولة مرة أخرى.";
        messageClass.value = "bg-red-100 text-red-800 border border-red-300";
        availSlots.value = [];
      }
    }
  } else {
    loading.value = false;
  }
});
</script>

<style scoped>
input {
  background-color: white;
}
</style>
