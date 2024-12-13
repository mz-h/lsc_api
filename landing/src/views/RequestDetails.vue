<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div
      class="chat-container space-y-4 p-8 mx-0 my-auto bg-gray-200 rounded-box"
    >
      <div
        class="message flex flex-col gap-1"
        v-for="(message, index) in messages"
        :key="index"
      >
        <span class="text-xs text-gray-500 text-center">{{
          message.time
        }}</span>
        <div class="flex flex-row items-start">
          <div
            class="icon bg-gray-100 w-11 h-8 flex justify-center items-center rounded-full p-0 m-0"
          >
            <img
              src="../assets/images/logo.png"
              width="15"
              height="15"
              alt=""
            />
          </div>

          <div class="bg-white p-4 mx-3 rounded-lg shadow w-full">
            <p class="text-gray-500">{{ message.text }}</p>
          </div>
        </div>
        <div
          class="bg-primaryMoreLight p-5 mx-16 mt-4 rounded-lg shadow flex flex-col justify-center items-center gap-2"
          v-if="message.type == 'sent'"
        >
          <h4 class="text-primary">ملخص القضية وعنوانها</h4>
          <div class="btns flex flex-row justify-center items-center gap-2">
            <button
              class="btn btn-secondry btn-sm bg-primary border-none hover:bg-primary text-white"
            >
              عرض</button
            ><button
              class="btn btn-secondry btn-sm bg-white hover:bg-white border-none text-gray-500"
            >
              لاحقًا
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      messages: [
        { time: "Wed 8:21 AM", text: "تم إرسال الطلب.", type: "summary" },
        { time: "Sun 2:00 PM", text: "تمت مراجعة الطلب.", type: "summary" },
        {
          time: "Sun 2:00 PM",
          text: "تم إرسال ملخص دراسة القضية. يرجى الاطلاع عليه.",
          type: "sent",
        },
        {
          time: "Sun 2:00 PM",
          text: 'ملخص دراسة القضية "عنوانها"',
          type: "summary",
          button: true,
          buttonText: "عرض",
        },
        {
          time: "Sun 2:00 PM",
          text: "يرجى توكيل المحامي بالتفاصيل.",
          type: "summary",
        },
      ],
    };
  },
  methods: {
    handleButtonClick() {
      alert("تم الضغط على زر العرض.");
    },
  },
};
</script>

<style scoped>
.chat-container {
  max-width: 400px;
  margin: 0 auto;
}

.message {
  width: 100%;
}
</style>
