import {
  View,
  Text,
  Image,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Alert,
} from "react-native";
import React, { useState, useEffect } from "react";
import { images } from "@/constants/images";
import { icons } from "@/constants/icons";
import { router } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
}

export default function Card() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const response = await fetch(
        `${process.env.EXPO_PUBLIC_API_URL}api/core/user/`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch user data");
      }

      const data = await response.json();
      setUser(data);
    } catch (err) {
      console.error("Error fetching user:", err);
      Alert.alert("Chyba", "Nepodarilo sa načítať používateľa");
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    Alert.alert("Skopírované", "IBAN bol skopírovaný do schránky");
  };

  if (loading) {
    return (
      <View className="flex-1 bg-black items-center justify-center">
        <ActivityIndicator size="large" color="#FFFFFF" />
      </View>
    );
  }

  return (
    <View className="flex-1 bg-black">
      <Image
        source={images.bg}
        className="absolute w-full h-full z-0"
        resizeMode="cover"
      />

      {/* Header */}
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
          Vaša karta
        </Text>
      </View>

      <ScrollView
        className="flex-1"
        contentContainerStyle={{ paddingBottom: 100 }}
      >
        <View className="px-6 pt-6">
          {/* Karta */}
          <View className="rounded-3xl overflow-hidden mb-6">
            <Image
              source={images.card}
              className="w-full h-48"
              resizeMode="cover"
            />
          </View>

          {/* Informácie karty */}
          <View className="bg-box rounded-3xl p-6 mb-6 border border-[#2a3550]">
            <Text className="text-white text-lg font-semibold mb-4">
              Informácie karty
            </Text>

            <View className="space-y-3">
              <View>
                <Text className="text-white/60 text-sm mb-1">
                  Držiteľ karty:
                </Text>
                <Text className="text-white text-base">
                  {user ? `${user.first_name} ${user.last_name}` : "N/A"}
                </Text>
              </View>

              <View>
                <Text className="text-white/60 text-sm mb-1">Číslo karty:</Text>
                <Text className="text-white text-base">**** 1236</Text>
              </View>
            </View>
          </View>

          {/* IBAN */}
          <TouchableOpacity
            activeOpacity={0.7}
            onPress={copyToClipboard}
            className="bg-box rounded-3xl p-6 border border-[#2a3550] flex-row items-center justify-between"
          >
            <View className="flex-1">
              <Text className="text-white/60 text-sm mb-1">IBAN:</Text>
              <Text className="text-white text-base">
                SK8975000000000012345671
              </Text>
            </View>
            <Ionicons name="copy-outline" size={24} color="#FFFFFF" />
          </TouchableOpacity>
        </View>
      </ScrollView>
    </View>
  );
}