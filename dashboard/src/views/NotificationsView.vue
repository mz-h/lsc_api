<template>
  <LoggedInTopNav title="الإشعارات" />
  <div class="notification container grid grid-cols-1 grid-rows-1 mt-20 pb-16">
    <div
      v-for="notification in notifications"
      :key="notification.name"
      class="bg-white border-solid border-1 border-gray-200 flex items-center gap-3 py-5 px-8 lg:px-20"
    >
      <div class="icon">
        <font-awesome-icon
          :icon="['fa-regular', 'fa-bell']"
          :class="{ 'text-red-500': hasNewNotifications }"
        />
      </div>
      <div class="content text-right text-sm flex flex-col gap-2">
        <h4 class="text-black" v-html="notification.subject"></h4>
        <p>{{ notification.creation }}</p>
      </div>
    </div>
  </div>
  <Loader v-if="loading" />
  <BottomNav />
</template>

<style scoped>
.text-red-500 {
  color: #ef4444; /* Tailwind CSS red color */
}
</style>

<script setup>
import Loader from "../components/Loader.vue";
import BottomNav from "../components/BottomNav.vue";
import LoggedInTopNav from "../components/LoggedInTopNav.vue";
import { ref, onMounted, onBeforeUnmount, inject } from "vue";
import { notificationsState } from "../router/notificationsState";

const notifications = ref([]);
// const hasNewNotifications = ref(false);

// // Inject the socket instance provided in main.js
// const socket = inject("$socket");
const loading = ref(false);
// Function to fetch notifications from the API
const getNotificationsData = async () => {
  loading.value = true;
  try {
    const response = await fetch(
      "/api/method/lsc_api.lsc_api.get_user_notifications.get_user_notifications"
    );
    if (!response.ok) {
      loading.value = false;
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    notifications.value = data.message;
    loading.value = false;
  } catch (error) {
    loading.value = false;
    console.error("Error fetching notifications:", error);
  }
};

// // Function to handle incoming real-time notifications
// const handleRealtimeNotifications = (data) => {
//   notifications.value = data.notifications;
//   hasNewNotifications.value = true; // Indicate that there are new notifications
//   console.log("socket update");
//   notificationsState.hasNewNotifications = true; // Update shared state
// };

// // Initialize socket listeners
// const setupSocketListeners = () => {
//   console.log("socket start");
//   if (socket) {
//     socket.on("user_notifications", handleRealtimeNotifications);
//     console.log("socket connected");
//   } else {
//     console.error("Socket instance not found!");
//   }
// };

// // Clean up socket listeners
// const cleanupSocketListeners = () => {
//   console.log("socket Off");
//   if (socket) {
//     socket.off("user_notifications", handleRealtimeNotifications);
//   }
// };

onMounted(() => {
  getNotificationsData();
  // setupSocketListeners();
});

// onBeforeUnmount(() => {
//   cleanupSocketListeners();
// });

// // Optional: Reset the bell icon color when notifications are viewed
// const markNotificationsAsViewed = () => {
//   hasNewNotifications.value = false;
// };
</script>
