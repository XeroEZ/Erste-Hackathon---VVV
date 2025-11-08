import {
  View,
  Text,
  Image,
  TouchableOpacity,
  ScrollView,
} from "react-native";
import React, { useState } from "react";
import { images } from "@/constants/images";
import { icons } from "@/constants/icons";
import { router } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

const categories = [
  { id: 1, name: "Zábava", amount: "35.09€", percentage: "5.15%", icon: icons.zabava },
  { id: 2, name: "Bez kategórie", amount: "35.09€", percentage: "5.15%", icon: icons.bezkategorie },
  { id: 3, name: "Auto a doprava", amount: "35.09€", percentage: "5.15%", icon: icons.auto },
  { id: 4, name: "Osobné", amount: "35.09€", percentage: "5.15%", icon: icons.osoba },
  { id: 5, name: "Denné výdavky", amount: "3500.09€", percentage: "5.15%", icon: icons.dennevydavky },
  { id: 6, name: "Platby", amount: "35.09€", percentage: "5.15%", icon: icons.platby },
  { id: 7, name: "Domácnosť", amount: "35.09€", percentage: "5.15%", icon: icons.domacnost },
];

export default function Expenses() {
  const [selectedYear] = useState(2025);

  return (
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />

      {/* Header - Fixed at top like in [id].tsx */}
      <View className="flex-row items-center px-5 pt-12 pb-4 border-b border-white/10">
        <TouchableOpacity onPress={() => router.back()} className="mr-4">
          <Image
            source={icons.back}
            className="w-6 h-6"
            tintColor="#FFFFFF"
            resizeMode="contain"
          />
        </TouchableOpacity>
        <Text className="text-white text-lg font-semibold flex-1">
          Výdavky
        </Text>
      </View>

      <ScrollView 
        className="flex-1"
        contentContainerStyle={{ paddingBottom: 100 }}
      >
        <View className="px-6 pt-6">
          {/* Vaše výdavky card */}
          <View className="bg-[#1a1f3a] rounded-3xl p-6 mb-6 border border-[#2a3550]">
            <Text className="text-white/60 text-sm mb-2">Vaše výdavky</Text>
            <Text className="text-white text-4xl font-bold mb-4">100,000€</Text>

            {/* Graf placeholder */}
            <View className="bg-black rounded-2xl h-32 items-center justify-center">
              <Text className="text-white text-xl font-semibold">GRAF</Text>
            </View>
          </View>

          {/* Mesiac selector */}
          <View className="flex-row items-center justify-between mb-6 bg-[#1a1f3a] rounded-full px-4 py-3 border border-[#2a3550]">
            <TouchableOpacity className="w-10 h-10 items-center justify-center">
              <Ionicons name="chevron-back" size={24} color="white" />
            </TouchableOpacity>
            <Text className="text-white text-lg font-semibold">
              Mesiac {selectedYear}
            </Text>
            <TouchableOpacity className="w-10 h-10 items-center justify-center">
              <Ionicons name="chevron-forward" size={24} color="white" />
            </TouchableOpacity>
          </View>

          {/* Kategórie header */}
          <View className="mb-4">
            <Text className="text-white text-lg font-semibold">Kategórie</Text>
          </View>

          {/* Kategórie list */}
          <View>
            {categories.map((category) => (
              <TouchableOpacity
                key={category.id}
                activeOpacity={0.7}
                className="flex-row items-center bg-[#1a1f3a] rounded-2xl p-4 mb-3 border border-[#2a3550]"
              >
                <View className="w-12 h-12 rounded-full bg-white/10 items-center justify-center mr-4">
                  <Image
                    source={category.icon}
                    className="w-7 h-7"
                    resizeMode="contain"
                  />
                </View>
                <View className="flex-1">
                  <Text className="text-white text-base font-medium">
                    {category.name}
                  </Text>
                </View>
                <View className="items-end">
                  <Text className="text-white text-lg font-semibold">
                    {category.amount}
                  </Text>
                  <Text className="text-white/50 text-xs">
                    {category.percentage}
                  </Text>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        </View>
      </ScrollView>
    </View>
  );
}