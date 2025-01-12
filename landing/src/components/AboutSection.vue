<script setup>
import SectionTitle from "./SectionTitle.vue";
import { useI18n } from "vue-i18n";
const { t } = useI18n();
import LinkeinWhite from "../assets/icons/l-w.svg";
import TwitterWhite from "../assets/icons/x-w.svg";
import FacebookWhite from "../assets/icons/f-w.svg";
import InstagramWhite from "../assets/icons/i-w.svg";

</script>

<template>
  <section
  :dir="$i18n.locale == 'ar' ? 'rtl' : 'ltr'"

    class="about w-full px-4 min-h-screen lg:min-h-full 3xl:min-h-screen flex flex-col justify-center items-center"
    id="about"
  >
    <SectionTitle :title="t('About')" />
    <div
      class="flex flex-col w-full my-6 gap-4 lg:flex-row lg:space-y-0 lg:w-4/5 mx-auto"
    >
      <div class="about-img lg:w-1/2">
        <img
          class="w-full h-full object-cover  block rounded-t-2xl lg:rounded-2xl"
          src="../assets/images/work-2.jpg"
          alt=""
        />
      </div>
      <div
        class="about-content bg-white rounded-b-2xl lg:rounded-2xl px-6 py-4 flex flex-col justify-center items-center space-y-4 lg:w-1/2 lg:items-start lg:justify-between"
      >
        <h2 class="text-3xl font-semibold border-b border-primary pb-2">
          {{ $t("AboutSection.title") }}
        </h2>
        <p class="text-justify font-light">
          {{ $t("AboutSection.titleTextp1") }}
          <br />
          {{ $t("AboutSection.titleTextp2") }}
        </p>
        <h2 class="text-3xl font-semibold border-b border-primary pb-2">
          {{ $t("AboutSection.vision") }}
        </h2>
        <p class="text-justify font-light">
          {{ $t("AboutSection.visionText") }}
        </p>
        <h2 class="text-3xl font-semibold border-b border-primary pb-2">
          {{ $t("AboutSection.mission") }}
        </h2>
        <p class="text-justify font-light">
          {{ $t("AboutSection.missionText") }}
        </p>
        <div class="social-links flex gap-4">
          <a href="https://www.facebook.com/share/18kYp9EtSC/?mibextid=wwXIfr">
            <img
              width="25"
              height="25"
              :src="FacebookWhite"
              alt="facebook--v1"
            />
          </a>
          <a href="https://x.com/musanadasa">
            <img
              width="25"
              height="25"
              :src="TwitterWhite"
              alt="twitterx--v1"
            />
          </a>
          <a href="https://www.instagram.com/musanadasa/">
            <img
              width="25"
              height="25"
              :src="InstagramWhite"
              alt="instagram-new--v1"
            />
          </a>
          <a href="https://www.linkedin.com/company/musanadahsa/">
            <img
              width="25"
              height="25"
              :src="LinkeinWhite"
              alt="LinkedIn--v1"
            />
          </a>
        </div>
        <div class="about-cta flex gap-4 items-center">
          <a
            class="btn py-2 px-8 bg-primary border-primary text-white"
            href="https://portal.lsc-sa.net/dashboard"
          >
            {{ $t("AboutSection.requestService") }}
        </a>
        </div>
      </div>
    </div>
  </section>
</template>



<style scoped>
.social-links a {
  padding: 8px;
  border: 1px solid transparent;
  background-color: #354f88;
  border-radius: 8px;
  transition: all 0.3s;
}
.social-links a:hover {
  padding: 8px;
  border: 1px solid #223458;
  background-color: #223458;
  border-radius: 8px;
}
</style>
