import { icons } from "@/constants/icons";
import { images } from "@/constants/images";
import { Tabs } from "expo-router";
import React from "react";
import { Image, ImageBackground, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

const TabIcon = ({ focused, icon }: any) => {
  if (focused) {
    return (
      <ImageBackground
        source={images.highlight}
        className="flex flex-row w-full flex-1 min-w-[80px] min-h-14 mt-4 justify-center items-center rounded-full overflow-hidden"
      >
        <Image source={icon} tintColor="#FFFFFF" className="size-8" />
      </ImageBackground>
    );
  }
  return (
    <View className="size-full justify-center items-center mt-4 rounded-full">
      <Image source={icon} tintColor="#8D8D8D" className="size-8" />;
    </View>
  );
};

const _layout = () => {
  return (
    <Tabs
      screenOptions={{
        tabBarShowLabel: false,
        tabBarItemStyle: {
          width: "100%",
          height: "100%",
          justifyContent: "center",
          alignItems: "center",
        },
        tabBarStyle: {
          backgroundColor: "#272727",
          borderRadius: 70,
          marginHorizontal: 20,
          marginBottom: 20,
          height: 53,
          position: "absolute",
          overflow: "hidden",
          borderWidth: 0.5,
          borderColor: "#898989",
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          headerShown: false,
          title: "Banking",
          tabBarIcon: ({ focused }) => (
            <TabIcon focused={focused} icon={icons.banking} />
          ),
        }}
      />
      <Tabs.Screen
        name="chatbot"
        options={{
          headerShown: false,
          title: "Chatbot",
          tabBarIcon: ({ focused }) => (
            <TabIcon focused={focused} icon={icons.chatbot} />
          ),
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          headerShown: false,
          title: "Settings",
          tabBarIcon: ({ focused }) => (
            <TabIcon focused={focused} icon={icons.settings} />
          ),
        }}
      />
    </Tabs>
  );
};

export default _layout;
