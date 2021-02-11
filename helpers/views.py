def view_summary_daily(data):
    # WIDGET TITLE SECTION
    html = (
        """
        <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="30"></td> </tr> <!--end white spacing-->
       <!--full text title-->
       <tr bgcolor="#fff" >
           <td align="center">
               <p style="font-family: Helvetica, arial, sans-serif; font-size: 20px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 60px;">
                   """
        + data["title"]
        + """
               </p>
           </td>
       </tr>
       <!--end full text title-->
        <!--full text content-->
        <tr bgcolor="#fff" >
            <td align="center">
                <table class="full" cellpadding="5" cellspacing="0">
                    <tbody>
                        <tr>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][0][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][0][0])
        + """</span>
                            </td>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][1][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][1][0])
        + """</span>
                            </td>
                        </tr>
                        <tr>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][2][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][2][0])
        + """</span>
                            </td>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][3][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][3][0])
        + """</span>
                            </td>
                        </tr>
                        <tr>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][4][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][4][0])
        + """</span>
                            </td>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][5][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][5][0])
        + """</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <!--end full text content-->
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
        <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
        """
    )

    return html


def view_summary_monthly(data):
    # WIDGET TITLE SECTION
    html = (
        """
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="30"></td> </tr> <!--end white spacing-->
        <!--full text title-->
        <tr bgcolor="#fff" >
            <td align="center">
                <p style="font-family: Helvetica, arial, sans-serif; font-size: 20px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 60px; line-height:30px;">
                    """
        + data["title"]
        + """
                </p>
            </td>
        </tr>
        <!--end full text title-->
        <!--full text content-->
        <tr bgcolor="#fff" >
            <td align="center">
                <table class="full" cellpadding="5" cellspacing="0">
                    <tbody>
                        <tr>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][0][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][0][0])
        + """</span>
                            </td>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][1][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][1][0])
        + """</span>
                            </td>
                        </tr>
                        <tr>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][2][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][2][0])
        + """</span>
                            </td>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][3][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][3][0])
        + """</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <!--end full text content-->
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
        <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
        """
    )

    return html


def view_summary_quarter(data):
    # WIDGET TITLE SECTION
    html = (
        """
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="30"></td> </tr> <!--end white spacing-->
        <!--full text title-->
        <tr bgcolor="#fff" >
            <td align="center">
                <p style="font-family: Helvetica, arial, sans-serif; font-size: 20px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 60px; line-height:30px;">
                    """
        + data["title"]
        + """
                </p>
            </td>
        </tr>
        <!--end full text title-->
        <!--full text content-->
        <tr bgcolor="#fff" >
            <td align="center">
                <table class="full" cellpadding="5" cellspacing="0">
                    <tbody>
                        <tr>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][0][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][0][0])
        + """</span>
                            </td>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][1][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][1][0])
        + """</span>
                            </td>
                        </tr>
                        <tr>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][2][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][2][0])
        + """</span>
                            </td>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records"][3][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records"][3][0])
        + """</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <!--end full text content-->
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
        <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
        
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="30"></td> </tr> <!--end white spacing-->
        <!--full text title-->
        <tr bgcolor="#fff" >
            <td align="center">
                <p style="font-family: Helvetica, arial, sans-serif; font-size: 20px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 60px; line-height:30px;">
                    """
        + data["title1"]
        + """
                </p>
            </td>
        </tr>
        <!--end full text title-->
        <!--full text content-->
        <tr bgcolor="#fff" >
            <td align="center">
                <table class="full" cellpadding="5" cellspacing="0">
                    <tbody>
                        <tr>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records1"][0][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records1"][0][0])
        + """</span>
                            </td>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records1"][1][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records1"][1][0])
        + """</span>
                            </td>
                        </tr>
                        <tr>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records1"][2][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records1"][2][0])
        + """</span>
                            </td>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records1"][3][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records1"][3][0])
        + """</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <!--end full text content-->
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
        <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
        
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="30"></td> </tr> <!--end white spacing-->
        <!--full text title-->
        <tr bgcolor="#fff" >
            <td align="center">
                <p style="font-family: Helvetica, arial, sans-serif; font-size: 20px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 60px; line-height:30px;">
                    """
        + data["title2"]
        + """
                </p>
            </td>
        </tr>
        <!--end full text title-->
        <!--full text content-->
        <tr bgcolor="#fff" >
            <td align="center">
                <table class="full" cellpadding="5" cellspacing="0">
                    <tbody>
                        <tr>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records2"][0][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records2"][0][0])
        + """</span>
                            </td>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records2"][1][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records2"][1][0])
        + """</span>
                            </td>
                        </tr>
                        <tr>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records2"][2][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records2"][2][0])
        + """</span>
                            </td>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records2"][3][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records2"][3][0])
        + """</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <!--end full text content-->
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
        <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
        
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="30"></td> </tr> <!--end white spacing-->
        <!--full text title-->
        <tr bgcolor="#fff" >
            <td align="center">
                <p style="font-family: Helvetica, arial, sans-serif; font-size: 20px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 60px; line-height:30px;">
                    """
        + data["title3"]
        + """
                </p>
            </td>
        </tr>
        <!--end full text title-->
        <!--full text content-->
        <tr bgcolor="#fff" >
            <td align="center">
                <table class="full" cellpadding="5" cellspacing="0">
                    <tbody>
                        <tr>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records3"][0][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records3"][0][0])
        + """</span>
                            </td>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records3"][1][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records3"][1][0])
        + """</span>
                            </td>
                        </tr>
                        <tr>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records3"][2][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records3"][2][0])
        + """</span>
                            </td>
                            <td valign="top" style="text-align:center;border-collapse:collapse;font-family:Helvetica,Arial,sans-serif;line-height:20px;width:50%;padding-bottom:30px">
                                <span style="font-size:32px;font-weight:normal;color:#0585f9">"""
        + str(data["records3"][3][1])
        + """</span><br>
                                <span style="font-size:14px;font-weight:bold;color:#414141">"""
        + str(data["records3"][3][0])
        + """</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <!--end full text content-->
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
        <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
        """
    )

    return html


def view_distribute(data):
    # WIDGET TITLE SECTION
    html = (
        """
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="30"></td> </tr> <!--end white spacing-->
        <!--full text title-->
        <tr bgcolor="#fff" >
            <td align="center">
                <p style="font-family: Helvetica, arial, sans-serif; font-size: 20px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 20px;">
                    """
        + data["title"]
        + """
                </p>
            </td>
        </tr>
        <!--end full text title-->"""
    )

    if "chart" in data:
        html += (
            """
            <!--chart-->
            <tr bgcolor="#fff" >
                <td align="center">
                    <table>
                        <tbody>
                            <tr>
                                <td>
                                    <div class="container" align="center">
                                        <br/>
                                        <img src=\""""
            + data["chart"]
            + """\" alt="chart title" width="450">
                                        <br/><br/><br/><br/>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            <!--end chart-->"""
        )

    html += """
        <!--full text content-->
        <tr bgcolor="#fff" >
            <td align="center">
                <table class="full" cellpadding="5" cellspacing="0">
                    <thead>
                        <tr style="font-family: Helvetica, arial, sans-serif; font-size: 12px; color: #8997a2; line-height: 20px; font-weight:300;">"""

    # WIDGET TABLE HEADER
    iteration = 0
    for item in data["table_headers"]:
        if iteration == 0:
            html += (
                """<td style="border: none;border-bottom: solid 1px #ccc;text-align: center;">%s</td>"""
                % item
            )
        elif iteration == 1:
            html += (
                """<td style="border: none;border-bottom: solid 1px #ccc;text-align: left;">%s</td>"""
                % item
            )
        else:
            html += (
                """<td style="border: none;border-bottom: solid 1px #ccc;text-align: right;">%s</td>"""
                % item
            )
        iteration += 1
    html += """</tr></thead><tbody>"""

    rownum = 1
    for row in data["records"]:

        if rownum <= 3:
            html += """<tr style="font-family: Helvetica, arial, sans-serif; font-size: 14px; color: #333; text-align:left; line-height: 20px; font-weight:800;">"""
        else:
            html += """<tr style="font-family: Helvetica, arial, sans-serif; font-size: 14px; color: #333; text-align:left; line-height: 20px; font-weight:400;">"""

        iteration = 0
        for column in row:

            if iteration == 0:
                html += (
                    """<td style="border: none;border-bottom: solid 1px #ccc;text-align: center;">%s</td>"""
                    % column
                )
            elif iteration == 1:
                html += (
                    """<td style="border: none;border-bottom: solid 1px #ccc;text-align: left;">%s</td>"""
                    % column
                )
            else:
                html += (
                    """<td style="border: none;border-bottom: solid 1px #ccc;text-align: right;">%s</td>"""
                    % column
                )
            iteration += 1
        rownum += 1

    html += """</tr></tbody>"""

    if "table_footer" in data:
        html += (
            """<tfoot>
                        <tr style="font-family: Helvetica, arial, sans-serif; font-size: 10px; color: #333; line-height: 20px; font-weight:400;">
                            <td></td>
                            <td style="text-align: left;"> %s </td>
                            <td></td>
                            <td></td>
                        </tr>
                    </tfoot>"""
            % data["table_footer"]
        )

    html += """         </table>
                    </td>
                </tr>
                <!--end full text content-->
                <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
                <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
                """

    return html


def view_distribute_expense(data):
    # WIDGET TITLE SECTION
    html = (
        """
        <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="30"></td> </tr> <!--end white spacing-->
        <!--full text title-->
        <tr bgcolor="#fff" >
            <td align="center">
                <p style="font-family: Helvetica, arial, sans-serif; font-size: 20px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 20px;">
                    """
        + data["title"]
        + """
                </p>
            </td>
        </tr>
        <!--end full text title-->"""
    )

    html += """
        <!--full text content-->
        <tr bgcolor="#fff" >
            <td align="center">
                <table class="full" cellpadding="5" cellspacing="0">
                    <thead>
                        <tr style="font-family: Helvetica, arial, sans-serif; font-size: 12px; color: #8997a2; line-height: 20px; font-weight:300;">"""

    # WIDGET TABLE HEADER
    iteration = 0
    for item in data["table_headers"]:
        if iteration == 0:
            html += (
                """<td style="border: none;border-bottom: solid 1px #ccc;text-align: center;">%s</td>"""
                % item
            )
        elif iteration == 1:
            html += (
                """<td style="border: none;border-bottom: solid 1px #ccc;text-align: left;">%s</td>"""
                % item
            )
        else:
            html += (
                """<td style="border: none;border-bottom: solid 1px #ccc;text-align: right;">%s</td>"""
                % item
            )
        iteration += 1
    html += """</tr></thead><tbody>"""

    number_of_expense = len(data["records"])
    rownum = 1
    for row in data["records"]:

        # JIKA FOR LOOP SUDAH MENCAPAI BARIS TERAKHIR (GRAND TOTAL)
        # MAKA CETAK TEBAL BARIS TERSEBUT
        if number_of_expense == rownum:
            html += """<tr style="font-family: Helvetica, arial, sans-serif; font-size: 14px; color: #333; text-align:left; line-height: 20px; font-weight:800;">"""
        else:
            html += """<tr style="font-family: Helvetica, arial, sans-serif; font-size: 14px; color: #333; text-align:left; line-height: 20px; font-weight:400;">"""

        iteration = 0
        for column in row:
            if iteration == 0:
                html += (
                    """<td style="border: none;border-bottom: solid 1px #ccc;text-align: center;">%s</td>"""
                    % column
                )
            elif iteration == 1:
                html += (
                    """<td style="border: none;border-bottom: solid 1px #ccc;text-align: left;">%s</td>"""
                    % column
                )
            else:
                html += (
                    """<td style="border: none;border-bottom: solid 1px #ccc;text-align: right;">%s</td>"""
                    % column
                )
            iteration += 1
        rownum += 1

    html += """</tr></tbody>"""

    if "table_footer" in data:
        html += (
            """<tfoot>
                        <tr style="font-family: Helvetica, arial, sans-serif; font-size: 10px; color: #333; line-height: 20px; font-weight:400;">
                            <td></td>
                            <td style="text-align: left;"> %s </td>
                            <td></td>
                            <td></td>
                        </tr>
                    </tfoot>"""
            % data["table_footer"]
        )

    html += """         </table>
                    </td>
                </tr>
                <!--end full text content-->
                <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
                <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
                """

    return html


def view_no_data(widget_title):
    html = (
        """
            <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
            <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
            <tr bgcolor="#fff" >
                <td align="center">
                    <p style="font-family: Helvetica, arial, sans-serif; font-size: 20px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 20px; line-height:30px;">
                        """
        + widget_title
        + """
                    </p>
                </td>
            </tr>
            <tr bgcolor="#fff" >
                <td align="center">
                    <img src="http://cdn.revota.com/raven3/no-data.jpg">

                    <p style="font-family: Helvetica, arial, sans-serif; font-size: 14px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 20px;">
                        No Data Available
                    </p>
                </td>
            </tr>
            <!--end full text title-->
            <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
            <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
        """
    )

    return html


def view_no_data_quarter(widget_title, widget_title1, widget_title2, widget_title3):
    html = (
        """
            <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
            <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
            <tr bgcolor="#fff" >
                <td align="center">
                    <p style="font-family: Helvetica, arial, sans-serif; font-size: 20px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 20px; line-height:30px;">
                        """
        + widget_title
        + """
                    </p>
                </td>
            </tr>
            <tr bgcolor="#fff" >
                <td align="center">
                    <img src="http://cdn.revota.com/raven3/no-data.jpg">

                    <p style="font-family: Helvetica, arial, sans-serif; font-size: 14px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 20px;">
                        No Data Available
                    </p>
                </td>
            </tr>
            <!--end full text title-->
            <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
            <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->

            <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
            <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
            <tr bgcolor="#fff" >
                <td align="center">
                    <p style="font-family: Helvetica, arial, sans-serif; font-size: 20px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 20px; line-height:30px;">
                        """
        + widget_title1
        + """
                    </p>
                </td>
            </tr>
            <tr bgcolor="#fff" >
                <td align="center">
                    <img src="http://cdn.revota.com/raven3/no-data.jpg">

                    <p style="font-family: Helvetica, arial, sans-serif; font-size: 14px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 20px;">
                        No Data Available
                    </p>
                </td>
            </tr>
            <!--end full text title-->
            <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
            <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->

            <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
            <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
            <tr bgcolor="#fff" >
                <td align="center">
                    <p style="font-family: Helvetica, arial, sans-serif; font-size: 20px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 20px; line-height:30px;">
                        """
        + widget_title2
        + """
                    </p>
                </td>
            </tr>
            <tr bgcolor="#fff" >
                <td align="center">
                    <img src="http://cdn.revota.com/raven3/no-data.jpg">

                    <p style="font-family: Helvetica, arial, sans-serif; font-size: 14px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 20px;">
                        No Data Available
                    </p>
                </td>
            </tr>
            <!--end full text title-->
            <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
            <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->

            <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
            <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
            <tr bgcolor="#fff" >
                <td align="center">
                    <p style="font-family: Helvetica, arial, sans-serif; font-size: 20px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 20px; line-height:30px;">
                        """
        + widget_title3
        + """
                    </p>
                </td>
            </tr>
            <tr bgcolor="#fff" >
                <td align="center">
                    <img src="http://cdn.revota.com/raven3/no-data.jpg">

                    <p style="font-family: Helvetica, arial, sans-serif; font-size: 14px; color: #333; text-align:center; font-weight:400; padding: 20px 0px 20px;">
                        No Data Available
                    </p>
                </td>
            </tr>
            <!--end full text title-->
            <!--white spacing--> <tr bgcolor="#fff"> <td width="100%" height="20"></td> </tr> <!--end white spacing-->
            <!--blank spacing--> <tr> <td width="100%" height="30"></td> </tr> <!--end blank spacing-->
        """
    )

    return html