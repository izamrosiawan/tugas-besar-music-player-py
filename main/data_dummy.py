import os

def load_dummy_data(player):
    
    music_folder = r"C:\Users\LENOVO\Downloads\music-tubes"
    
    taylor = player.library.add_artist("Taylor Swift")
    taylor.add_song(1, "Shake It Off", "3:39", 
                   os.path.join(music_folder, "taylor_swift_shake_it_off.mp3"), "Pop")
    taylor.add_song(2, "Blank Space", "3:51", 
                   os.path.join(music_folder, "taylor_swift_blank_space.mp3"), "Pop")
    taylor.add_song(3, "Style", "3:51", 
                   os.path.join(music_folder, "taylor_swift_style.mp3"), "Pop")
    taylor.add_song(4, "Love Story", "3:56", 
                   os.path.join(music_folder, "taylor_swift_love_story.mp3"), "Pop")
    taylor.add_song(5, "Anti-Hero", "3:21", 
                   os.path.join(music_folder, "taylor_swift_anti_hero.mp3"), "Pop")
    
    ed = player.library.add_artist("Ed Sheeran")
    ed.add_song(6, "Shape of You", "3:53", 
               os.path.join(music_folder, "ed_sheeran_shape_of_you.mp3"), "Pop")
    ed.add_song(7, "Perfect", "4:23", 
               os.path.join(music_folder, "ed_sheeran_perfect.mp3"), "Pop")
    ed.add_song(8, "Castle on the Hill", "4:21", 
               os.path.join(music_folder, "ed_sheeran_castle_on_the_hill.mp3"), "Pop")
    ed.add_song(9, "Thinking Out Loud", "4:41", 
               os.path.join(music_folder, "ed_sheeran_thinking_out_loud.mp3"), "Pop")
    
    ariana = player.library.add_artist("Ariana Grande")
    ariana.add_song(10, "7 rings", "2:58", 
                   os.path.join(music_folder, "ariana_grande_7_rings.mp3"), "Pop")
    ariana.add_song(11, "thank u, next", "3:27", 
                   os.path.join(music_folder, "ariana_grande_thank_u_next.mp3"), "Pop")
    ariana.add_song(12, "positions", "2:52", 
                   os.path.join(music_folder, "ariana_grande_positions.mp3"), "Pop")
    
    dua = player.library.add_artist("Dua Lipa")
    dua.add_song(13, "Levitating", "3:23", 
                os.path.join(music_folder, "dua_lipa_levitating.mp3"), "Pop")
    dua.add_song(14, "Don't Start Now", "3:03", 
                os.path.join(music_folder, "dua_lipa_dont_start_now.mp3"), "Pop")
    dua.add_song(15, "New Rules", "3:29", 
                os.path.join(music_folder, "dua_lipa_new_rules.mp3"), "Pop")
    
    coldplay = player.library.add_artist("Coldplay")
    coldplay.add_song(16, "Adventure of a Lifetime", "4:23", 
                     os.path.join(music_folder, "coldplay_adventure_of_a_lifetime.mp3"), "Rock")
    coldplay.add_song(17, "Hymn for the Weekend", "4:18", 
                     os.path.join(music_folder, "coldplay_hymn_for_the_weekend.mp3"), "Rock")
    coldplay.add_song(18, "Viva La Vida", "4:01", 
                     os.path.join(music_folder, "coldplay_viva_la_vida.mp3"), "Rock")
    coldplay.add_song(19, "Fix You", "4:54", 
                     os.path.join(music_folder, "coldplay_fix_you.mp3"), "Rock")
    
    imagine = player.library.add_artist("Imagine Dragons")
    imagine.add_song(20, "Believer", "3:24", 
                    os.path.join(music_folder, "imagine_dragons_believer.mp3"), "Rock")
    imagine.add_song(21, "Thunder", "3:07", 
                    os.path.join(music_folder, "imagine_dragons_thunder.mp3"), "Rock")
    imagine.add_song(22, "Whatever It Takes", "3:21", 
                    os.path.join(music_folder, "imagine_dragons_whatever_it_takes.mp3"), "Rock")
    imagine.add_song(23, "Radioactive", "3:06", 
                    os.path.join(music_folder, "imagine_dragons_radioactive.mp3"), "Rock")
    
    onerepublic = player.library.add_artist("OneRepublic")
    onerepublic.add_song(24, "Counting Stars", "4:17", 
                        os.path.join(music_folder, "onerepublic_counting_stars.mp3"), "Rock")
    onerepublic.add_song(25, "Apologize", "3:28", 
                        os.path.join(music_folder, "onerepublic_apologize.mp3"), "Rock")
    onerepublic.add_song(26, "Good Life", "4:12", 
                        os.path.join(music_folder, "onerepublic_good_life.mp3"), "Rock")
    
    maroon5 = player.library.add_artist("Maroon 5")
    maroon5.add_song(27, "Sugar", "3:55", 
                    os.path.join(music_folder, "maroon_5_sugar.mp3"), "Pop")
    maroon5.add_song(28, "Girls Like You", "3:55", 
                    os.path.join(music_folder, "maroon_5_girls_like_you.mp3"), "Pop")
    maroon5.add_song(29, "Memories", "3:09", 
                    os.path.join(music_folder, "maroon_5_memories.mp3"), "Pop")
    
    weeknd = player.library.add_artist("The Weeknd")
    weeknd.add_song(30, "Starboy", "3:50", 
                   os.path.join(music_folder, "the_weeknd_starboy.mp3"), "R&B")
    weeknd.add_song(31, "Blinding Lights", "3:22", 
                   os.path.join(music_folder, "the_weeknd_blinding_lights.mp3"), "R&B")
    weeknd.add_song(32, "Save Your Tears", "3:35", 
                   os.path.join(music_folder, "the_weeknd_save_your_tears.mp3"), "R&B")
    weeknd.add_song(33, "Die For You", "4:20", 
                   os.path.join(music_folder, "the_weeknd_die_for_you.mp3"), "R&B")
    
    bruno = player.library.add_artist("Bruno Mars")
    bruno.add_song(34, "24K Magic", "3:46", 
                  os.path.join(music_folder, "bruno_mars_24k_magic.mp3"), "R&B")
    bruno.add_song(35, "That's What I Like", "3:26", 
                  os.path.join(music_folder, "bruno_mars_thats_what_i_like.mp3"), "R&B")
    bruno.add_song(36, "Uptown Funk", "4:30", 
                  os.path.join(music_folder, "bruno_mars_uptown_funk.mp3"), "R&B")
    
    sza = player.library.add_artist("SZA")
    sza.add_song(37, "Kill Bill", "2:33", 
                os.path.join(music_folder, "sza_kill_bill.mp3"), "R&B")
    sza.add_song(38, "Good Days", "4:39", 
                os.path.join(music_folder, "sza_good_days.mp3"), "R&B")
    sza.add_song(39, "I Hate U", "2:53", 
                os.path.join(music_folder, "sza_i_hate_u.mp3"), "R&B")
    
    billie = player.library.add_artist("Billie Eilish")
    billie.add_song(40, "bad guy", "3:14", 
                   os.path.join(music_folder, "billie_eilish_bad_guy.mp3"), "Alternative")
    billie.add_song(41, "when the party's over", "3:16", 
                   os.path.join(music_folder, "billie_eilish_when_the_partys_over.mp3"), "Alternative")
    billie.add_song(42, "Happier Than Ever", "4:58", 
                   os.path.join(music_folder, "billie_eilish_happier_than_ever.mp3"), "Alternative")
    
    arctic = player.library.add_artist("Arctic Monkeys")
    arctic.add_song(43, "Do I Wanna Know?", "4:32", 
                   os.path.join(music_folder, "arctic_monkeys_do_i_wanna_know.mp3"), "Alternative")
    arctic.add_song(44, "505", "4:13", 
                   os.path.join(music_folder, "arctic_monkeys_505.mp3"), "Alternative")
    arctic.add_song(45, "R U Mine?", "3:21", 
                   os.path.join(music_folder, "arctic_monkeys_r_u_mine.mp3"), "Alternative")
    
    calvin = player.library.add_artist("Calvin Harris")
    calvin.add_song(46, "Summer", "3:43", 
                   os.path.join(music_folder, "calvin_harris_summer.mp3"), "Electronic")
    calvin.add_song(47, "Feel So Close", "3:27", 
                   os.path.join(music_folder, "calvin_harris_feel_so_close.mp3"), "Electronic")
    
    drake = player.library.add_artist("Drake")
    drake.add_song(48, "God's Plan", "3:18", 
                  os.path.join(music_folder, "drake_gods_plan.mp3"), "Hip Hop")
    drake.add_song(49, "One Dance", "2:54", 
                  os.path.join(music_folder, "drake_one_dance.mp3"), "Hip Hop")
    drake.add_song(50, "Hotline Bling", "4:27", 
                  os.path.join(music_folder, "drake_hotline_bling.mp3"), "Hip Hop")
    
    eagles = player.library.add_artist("Eagles")
    eagles.add_song(51, "Hotel California", "6:30", 
                   os.path.join(music_folder, "eagles_hotel_california.mp3"), "Classic")
    eagles.add_song(52, "Take It Easy", "3:31", 
                   os.path.join(music_folder, "eagles_take_it_easy.mp3"), "Classic")
    
    bts = player.library.add_artist("BTS")
    bts.add_song(53, "Dynamite", "3:19", 
                os.path.join(music_folder, "bts_dynamite.mp3"), "K-Pop")
    bts.add_song(54, "Butter", "2:44", 
                os.path.join(music_folder, "bts_butter.mp3"), "K-Pop")
    bts.add_song(55, "Boy With Luv", "3:49", 
                os.path.join(music_folder, "bts_boy_with_luv.mp3"), "K-Pop")
    
    blackpink = player.library.add_artist("BLACKPINK")
    blackpink.add_song(56, "DDU-DU DDU-DU", "3:29", 
                      os.path.join(music_folder, "blackpink_ddu_du_ddu_du.mp3"), "K-Pop")
    blackpink.add_song(57, "How You Like That", "3:02", 
                      os.path.join(music_folder, "blackpink_how_you_like_that.mp3"), "K-Pop")
    blackpink.add_song(58, "Pink Venom", "3:07", 
                      os.path.join(music_folder, "blackpink_pink_venom.mp3"), "K-Pop")
    
    bad_bunny = player.library.add_artist("Bad Bunny")
    bad_bunny.add_song(59, "Tití Me Preguntó", "4:02", 
                      os.path.join(music_folder, "bad_bunny_titi_me_pregunto.mp3"), "Latin")
    bad_bunny.add_song(60, "Callaita", "4:10", 
                      os.path.join(music_folder, "bad_bunny_callaita.mp3"), "Latin")
