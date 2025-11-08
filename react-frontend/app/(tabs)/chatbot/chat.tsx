import { View, Text, Image, KeyboardAvoidingView } from "react-native";
import React, { useState } from "react";
import { images } from "@/constants/images";
import SearchBar from "@/components/SearchBar";
import { KeyboardAwareScrollView } from "react-native-keyboard-aware-scroll-view";
import ReccomendedPromptCard from "@/components/ReccomendedPromptCard";

const chat = () => {
  const [promptValue, setPromptValue] = useState("");

  return (
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />

      <View className="flex-1 justify-center items-center px-5">
        <Text className="text-xl text-white font-semibold">
          Niečo na inšpiráciu:
        </Text>
        <View className="flex-row flex-wrap justify-center max-w-sm">
          <View className="w-1/2 p-2">
            <ReccomendedPromptCard prompt="„Čo som kúpil včera“" color="pink" />
          </View>
          <View className="w-1/2 p-2">
            <ReccomendedPromptCard
              prompt="“Koľko som minul na topánky minulý rok”"
              color="green"
            />
          </View>
          <View className="w-1/2 p-2">
            <ReccomendedPromptCard prompt="„Mám psa?“" color="blue" />
          </View>
          <View className="w-1/2 p-2">
            <ReccomendedPromptCard prompt="Výdavky za január" color="red" />
          </View>
        </View>
      </View>

      {/* SearchBar with keyboard awareness - positioned absolutely at bottom */}
      <View className="absolute bottom-20 left-0 right-0 mx-5">
        <KeyboardAwareScrollView
          enableOnAndroid={true}
          keyboardShouldPersistTaps="handled"
          extraScrollHeight={150}
        >
          <View className="bg-accent rounded-lg py-3.5 flex flex-row justify-center items-center">
            <SearchBar
              placeholder="Zadaj svoju správu..."
              value={promptValue}
              onChangeText={setPromptValue}
            />
          </View>
        </KeyboardAwareScrollView>
      </View>
    </View>
  );
};

export default chat;
