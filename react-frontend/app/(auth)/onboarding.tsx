import { View, Text, Image, TouchableOpacity } from "react-native";
import React from "react";
import { images } from "@/constants/images";
import { router } from "expo-router";

const onboarding = () => {
  const goToSignIn = () => {
    router.push("/(auth)/signin");
  };

  return (
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />

      <Image
        source={images.welcome}
        className="absolute w-full h-1/2 top-0 z-10"
        resizeMode="cover"
      />

      <View className="absolute bottom-60 z-20 w-full px-4">
        <TouchableOpacity className="w-full" onPress={goToSignIn}>
          <Image
            source={images.signin}
            className="w-full h-12"
            resizeMode="contain"
          />
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default onboarding;
