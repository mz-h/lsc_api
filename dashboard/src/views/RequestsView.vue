<template>
  <LoggedInTopNav title="الطلبات" :backArrow="false" />
  <div
    class="bg-white mx-4 rounded mt-24 lg:mt-40 lg:mr-auto lg:ml-auto lg:w-1/2"
  >
    <div class="typeOfService flex items-center justify-center py-1">
      <span
        v-for="(req, index) in requests"
        :key="index"
        :class="{ activeService: activeIndex === index }"
        @click="setActive(index)"
      >
        {{ req }}
      </span>
    </div>
  </div>
  <div class="reqFilters flex gap-8 text-black items-center mx-4 mt-8">
    <div class="byMonth flex justify-between flex-grow">
      <select
        class="select select-bordered w-full select-xs select-ghost bg-gray-100 w-full text-black disabled:bg-gray-200 disabled:border-gray-200 disabled:text-black"
        id="month"
        v-model="selectedMonth"
      >
        <option v-for="month in monthsNames" :value="month.value">
          {{ month.name }}
        </option>
      </select>
    </div>
    <div class="byYear flex justify-between flex-grow">
      <select
        class="select select-bordered w-full select-xs select-ghost bg-gray-100 w-full text-black disabled:bg-gray-200 disabled:border-gray-200 disabled:text-black"
        id="month"
      >
        <option v-for="year in years" :value="year">
          {{ year }}
        </option>
      </select>
    </div>
  </div>

  <div v-if="availableRequests">
    <div
      class="openRequeust flex flex-col gap-4 mt-4 mb-4 overflow-y-scroll mx-4 lg:grid lg:grid-cols-3"
    >
      <div
        class="openReqCard flex flex-col gap-4 px-4 py-2 bg-white shadow-sm"
        v-for="(request, ind) in availableRequests.filter((e) => {
          if (selectedMonth) {
            return e.creation.split(' ')[0].split('-')[1] == selectedMonth;
          } else {
            return true;
          }
        })"
        :key="ind"
        @click="goToRequestDetails(request.name)"
      >
        <h2 class="reqCardType text-black">{{ request.item }}</h2>
        <ul class="leading-8 flex justify-between">
          <li>
            <p class="text-sm text-wrap">
              {{ request.status }}
            </p>
          </li>
          <li>
            <p class="text-sm text-wrap">
              {{ request.creation.split(" ")[0] }}
            </p>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div v-else>لا يوجد طلبات</div>
  <Loader v-if="loading" />
  <BottomNav />
</template>

<script setup>
import BottomNav from "@/components/BottomNav.vue";
import Loader from "@/components/Loader.vue";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const loading = ref(false);
const navigate = useRouter();
const requestOptions = {
  method: "GET",
  headers: { Cookie: document.cookie },
  redirect: "follow",
};
const monthsNames = [
  {
    name: "يناير",
    value: "01",
  },
  {
    name: "فبراير",
    value: "02",
  },
  {
    name: "مارس",
    value: "03",
  },
  {
    name: "أبريل",
    value: "04",
  },
  {
    name: "مايو",
    value: "05",
  },
  {
    name: "يونيو",
    value: "06",
  },
  {
    name: "يوليو",
    value: "07",
  },
  {
    name: "أغسطس",
    value: "08",
  },
  {
    name: "سبتمبر",
    value: "09",
  },
  {
    name: "أكتوبر",
    value: "10",
  },
  {
    name: "نوفمبر",
    value: "11",
  },
  {
    name: "ديسمبر",
    value: "12",
  },
];
const selectedMonth = ref("");
const years = ["2024"];

fetch("/api/method/frappe.auth.get_logged_user", requestOptions)
  .then((response) => {
    if (!response.ok) {
      throw new Error("You are not logged In");
    }
    return response.json();
  })
  .then()
  .catch(() => navigate.replace("/"));

const requests = ref(["حالياً", "سابقاً"]);
const availableRequests = ref([]);
const activeIndex = ref(0);

// Fake data for fallback
const fallbackCurrentRequests = [
  {
    type: "جلسة استشارة حضورية",
    title: "استشارة حول تطوير البرمجيات",
    date: "29 أغسطس 2024",
  },
  {
    type: "جلسة استشارة عن بعد",
    title: "استشارة في تصميم المواقع",
    date: "28 أغسطس 2024",
  },
  {
    type: "جلسة استشارة كتابية",
    title: "تحليل بيانات السوق",
    date: "27 أغسطس 2024",
  },
];
const fallbackPreviousRequests = [
  {
    type: "جلسة استشارة مرئية",
    title: "استشارة في إدارة المشاريع",
    date: "23 يوليو 2024",
  },
  {
    type: "جلسة استشارة حضورية",
    title: "استشارة حول تطوير التطبيقات",
    date: "15 يونيو 2024",
  },
  {
    type: "جلسة استشارة عن بعد",
    title: "استشارة في التسويق الرقمي",
    date: "10 مايو 2024",
  },
];

const router = useRouter(); // Initialize router

const fetchRequests = async () => {
  loading.value = true;
  try {
    let response;
    if (activeIndex.value === 0) {
      response = await axios.get(
        "/api/method/lsc_api.lsc_api.get_current_requests.get_current_requests"
      );
      loading.value = false;
      availableRequests.value =
        response.data.message.requests || fallbackCurrentRequests;
    } else {
      response = await axios.get(
        "/api/method/lsc_api.lsc_api.get_previous_requests.get_previous_requests"
      );
      loading.value = false;
      availableRequests.value =
        response.data.message.requests || fallbackPreviousRequests;
    }
  } catch (error) {
    loading.value = false;
    console.error("Failed to fetch requests:", error);
    availableRequests.value =
      activeIndex.value === 0
        ? fallbackCurrentRequests
        : fallbackPreviousRequests;
  }
};

const setActive = (index) => {
  activeIndex.value = index;
  fetchRequests();
};

const goToRequestDetails = (requestId) => {
  router.push({
    path: `/requests/requestDetails`,
    query: { requestId: requestId },
  });
};

onMounted(() => {
  fetchRequests();
});
</script>

<style scoped>
span {
  @apply text-primary w-full mx-2 my-2 py-2 flex justify-center text-nowrap rounded duration-300 cursor-pointer;
}

span.activeService {
  @apply bg-primary text-white font-body;
}
</style>
