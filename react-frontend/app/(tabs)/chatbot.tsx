import { View, Text, Image } from "react-native";
import React from "react";
import { images } from "@/constants/images";

const chatbot = () => {
  return (
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />
    </View>
  );
};

export default chatbot;
