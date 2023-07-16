def read_code(vs_info, shop_s, color_s, size_s):
      a_u_list = []
      shops = []
      colors = []
      sizes = []

      t = vs_info.replace("\"", "") + ","
      main_info = t.split("},")

      for m in range(len(main_info)-1):
         main_value = main_info[m].split(",(")
         shop_name = main_value[0].replace("{", "").strip()

         if shop_s == "" or shop_s == shop_name:
               shops.append(shop_name)

         shop = [shop_name]
         shop_node = []

         t = main_value[1].replace(")", "") + ","
         f_info = t.split(">,")
         
         for c in range(len(f_info)-1):
               f_value = f_info[c].split(",[")
               color_txt = f_value[0].replace("<", "").strip()

               if (not shop_s == "" and shop_s == shop_name) and \
               (color_s == "" or color_s == color_txt):
                  colors.append(color_txt)

               color = [color_txt]
               color_node = []

               t = f_value[1].replace("]", "") + ","
               s_info = t.split("|,")

               for s in range(len(s_info)-1):
                  s_value = s_info[s].split(", ")

                  if len(s_value) <= 1:
                     s_value = s_info[s].split(",")

                  s_n = []
                  for si in range(len(s_value)-1):
                     if (not shop_s == "" and shop_s == shop_name) and \
                     (not color_s == "" and color_s == color_txt) and \
                     (size_s == "" or size_s == s_value[si].replace("|", "").strip()):
                           if si == 0:
                              sizes.append(s_value[si].replace("|", "").strip())

                     s_n.append(s_value[si].replace("|", "").strip())

                  color_node.append(s_n)
               
               color.append(color_node)
               shop_node.append(color)

         shop.append(shop_node)
         a_u_list.append(shop)

      return shops, colors, sizes, a_u_list


def convert_string_to_nested_list(input_string):
    shops, colors, sizes, nested_list = read_code(input_string, "", "", "")
    return nested_list

print(convert_string_to_nested_list("\"{FLAG_SQUER,(<BROWN,[|XL, , 1, 0.0, , |]>)},\""))