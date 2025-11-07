import { View, Text, Image, TouchableOpacity } from "react-native";
import React from "react";
import { images } from "@/constants/images";
import { router } from "expo-router";

const signin = () => {
  const handleSignIn = () => {
    // UNTIL THE LOGIC IS IMPLEMENTED JUST PUT USER INTO THE APP
    router.replace("/(tabs)");
  };

  return (
    //console.log("Rendering Signin Screen"),
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />

      <View className="absolute bottom-60 z-20 w-full px-4 justify-center items-center">
        <TouchableOpacity className="w-full" onPress={handleSignIn}>
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

export default signin;
