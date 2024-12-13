<template>
  <LoggedInTopNav title="الطلبات" :backArrow="false" />
  <div class="bg-white mx-4 rounded mt-24 lg:mt-40">
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
      <p>نوفمبر</p>
      <img :src="arrowDownIcon" alt="Icon" />
    </div>
    <div class="byYear flex justify-between flex-grow">
      <p>2022</p>
      <img :src="arrowDownIcon" alt="Icon" />
    </div>
  </div>
  <div
    class="openRequeust flex flex-col gap-4 mt-4 mb-4 overflow-y-scroll mx-4"
  >
    <div
      class="openReqCard flex flex-col gap-4 px-4 py-2 bg-white shadow-sm"
      v-for="(ele, ind) in availableRequests"
      :key="ind"
       @click="goToRequestDetails(ind)"
    >
      <h2 class="reqCardType text-black">{{ ele.type }}</h2>
      <div class="cardRow flex justify-between text-sm">
        <p class="reqCardTitle text-primary">{{ ele.title }}</p>
        <p class="reqCardDate text-xs">{{ ele.date }}</p>
      </div>
    </div>
  </div>
  <BottomNav />

</template>

<script setup>
import BottomNav from "@/components/BottomNav.vue";
import { ref, onMounted } from "vue";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import arrowDownIcon from "../assets/images/icons/arrow_d_black.svg";
import axios from "axios";
import { useRouter } from 'vue-router';

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
  try {
    let response;
    if (activeIndex.value === 0) {
      response = await axios.get(
        "/api/method/lsc_api.lsc_api.get_current_requests.get_current_requests"
      );
      availableRequests.value =
        response.data.message || fallbackCurrentRequests;
    } else {
      response = await axios.get(
        "/api/method/lsc_api.lsc_api.get_previous_requests.get_previous_requests"
      );
      availableRequests.value =
        response.data.message || fallbackPreviousRequests;
    }
    // availableRequests.value = response.data.message;
    availableRequests.value = response.data.message; // Adjust the data structure as per your API response
  } catch (error) {
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

const goToRequestDetails = (index) => {
  // const selectedRequest = fallbackCurrentRequests.value[index];
  router.push({ name: 'RequestDetails', params: { id: index } });
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
